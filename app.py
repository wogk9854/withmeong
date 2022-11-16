from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.s7gsuon.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/')
def ho():
    return render_template('board/board.html')


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


@app.route("/board", methods=["GET"])
def board_road():
    board_list = list(db.board.find({}, {'_id': False}))
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


    return redirect(url_for("home"))


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

    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
