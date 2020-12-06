from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from parser_class import ParserClass
import uuid

app = Flask(__name__)
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
progress_ref = db.collection('progress')

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/url_parser/', methods=['POST'])
def form_post_endpoint():
    url = request.form['url']
    return redirect('/single_page_parser/' + url)

@app.route('/progress/<_id>')
def parsing_progress(_id):
    todo = progress_ref.document(_id).get()
    todo = todo.to_dict()
    print(todo)
    if todo is None:
        return {"status": 0, "message": "Loading..."}
    return {"status": todo["status"], 'message': todo["message"]}

@app.route('/single_page_parser/<url>')
def single_page_parser(url):
    url_parser = ParserClass(url, progress_ref)
    url_parser.start()
    url_parser.join()
    val_dict = url_parser.data
    _dict = {"status": 0, "message": ""}
    progress_ref.document(url).set(_dict)
    return render_template("url_parser.html", values=val_dict)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

