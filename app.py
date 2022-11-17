from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
from pymongo import MongoClient
import certifi

ca=certifi.where()


client = MongoClient('mongodb+srv://test:sparta@cluster0.s7gsuon.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

SECRET_KEY = 'SEVEN'
import jwt

import datetime
import hashlib

#홈화면
@app.route('/')
def home():
   return render_template('main.html')

@app.route('/board')
def ho():
    return render_template('board/board.html')
@app.route('/restaurant')
def restaurant():
    return render_template('with2.html')
@app.route('/cafe')
def cafe():
    return render_template('with.html')
@app.route('/pension')
def pension():
    return render_template('with3.html')

@app.route('/test')
def test():
    return render_template('nickname.html')

@app.route('/findid')
def findid():
    return render_template('login/findid.html')
@app.route('/findpw')
def findpw():
    return render_template('login/findpw.html')





@app.route('/write')
def main():
    return render_template('board/write.html')


@app.route("/board/write", methods=["POST"])
def board_post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    write_receive = request.form['write_give']
    board_list = list(db.board.find({}, {'_id': False}))
    num = len(board_list) + 1
    doc = {
        'title': title_receive,
        'content': content_receive,
        'write': write_receive,
        'num': num,
        'img':num
    }
    db.board.insert_one(doc)
    return jsonify({'msg': '작성완료'})


@app.route("/board/list", methods=["GET"])
def board_road():
    board_list = list(db.board.find({}, {'_id': False}))
    print(board_list)
    return jsonify({'board': board_list})


@app.route('/detail')
def detail():
    return render_template('board/detail.html')


@app.route("/upload_done", methods=["POST"])
def upload_done():
    board_list = list(db.board.find({}, {'_id': False}))
    num2 = len(board_list)
    print(num2)
    upload_files = request.files["file"]
    upload_files.save('static/img/{}.jpeg'.format(num2))


    return redirect(url_for("ho"))


@app.route("/save_num", methods=["POST"])
def save_num():
    global number
    number = request.form['num_give']

    return render_template('board/detail.html')


@app.route("/board_detail", methods=["GET"])
def board_detail():
    print(number)
    print(type(number))
    abc = int(number)
    print(type(abc))
    detail_board = db.board.find_one({'num': abc})
    print(detail_board)
    title = detail_board['title']
    write = detail_board['write']
    content = detail_board['content']
    num = detail_board['num']
    img = f"img/{abc}.jpeg"
    print(img)
    print(title, write, content)
    print(number)
    return jsonify({'title': title, 'write': write, 'content': content, 'num': num, 'img': img})

@app.route("/board_delete", methods=["POST"])
def board_delete():
    num = request.form['num_give']
    print(type(num))
    num1 = int(num)
    db.board.delete_one({'num':num1})

    return redirect(url_for("ho"))

@app.route("/board/comment", methods=["POST"])
def board_commnet():
    comment = request.form['comment_give']
    num = request.form['num_give']
    print(comment)
    print(num)
    write = '재하11'
    doc = {
        'comment':comment,
        'boardnum':num,
        'write':write

    }
    db.comment.insert_one(doc)

    return redirect(url_for("home"))


@app.route("/get_comment", methods=["GET"])
def get_comment():
    print('댓글')
    print(number)
    print(type(number))

    comment_list = list(db.comment.find({'boardnum': number}, {'_id': False}))

    return jsonify({'comment_list': comment_list})

#상정님 로그인부분 -----------------------------------------------------------------------------------
@app.route('/loginpage')
def loginpage():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.withmeong.find_one({"id": payload['id']})
        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login/login.html', msg=msg)

@app.route('/findid')
def find_id():
    return render_template('login/findid.html')

@app.route('/findpw')
def find_pw():
    return render_template('login/findpw.html')


@app.route('/register')
def register():
    return render_template('login/register.html')


@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']
    if db.withmeong.find_one({'id': id_receive}):
        return jsonify({'result': 'fail', 'msg': '이미 사용중인 이메일입니다.'})
        # driver.refresh()


    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.withmeong.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})


@app.route('/api/findid', methods=['POST'])
def api_find_id():
    findid_nick_receive = request.form['findid_nick_give']
    findid_pw_receive = request.form['findid_pw_give']

    findid_pw_hash = hashlib.sha256(findid_pw_receive.encode('utf-8')).hexdigest()

    if db.withmeong.find_one({'nick': findid_nick_receive, 'pw': findid_pw_hash}):
        user = db.withmeong.find_one({'nick': findid_nick_receive, 'pw': findid_pw_hash})
        user_id = user['id']
        print(user_id)
        return jsonify({'result': 'success', 'result_id': user_id})
    else:
        return jsonify({'result': 'fail'})

@app.route('/api/findpw', methods=['POST'])
def api_find_pw():
    findpw_email_receive = request.form['findpw_email_give']
    findpw_nick_receive = request.form['findpw_nick_give']

    print(findpw_email_receive, findpw_nick_receive)

    if db.withmeong.find_one({'id': findpw_email_receive, 'nick': findpw_nick_receive}):
        user = db.withmeong.find_one({'id': findpw_email_receive, 'nick': findpw_nick_receive})
        user_id = user['id']
        return jsonify({'result': 'success', 'result_id': user_id})
    else:
        print('fail')
        return jsonify({'msg':'msg'})

@app.route('/api/repw', methods=['POST'])
def api_re_pw():
    re_email = request.form['re_email_give']
    re_pw = request.form['re_pw_give']
    repw_hash = hashlib.sha256(re_pw.encode('utf-8')).hexdigest()
    db.withmeong.update_one({'id': re_email}, {'$set': {'pw': repw_hash}})

    return jsonify({'result': 'success'})

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.withmeong.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:

        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=20)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        print(token)
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '유효한 계정이 아닙니다.'})



# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        userinfo = db.withmeong.find_one({'id': payload['id']}, {'_id': 0})
        print(userinfo)
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)