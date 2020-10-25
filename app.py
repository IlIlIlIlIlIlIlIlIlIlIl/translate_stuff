# import argparse
from flask import Flask, render_template, request, redirect, url_for
from parser_class import ParserClass

app = Flask(__name__)
parse_progress = {}

@app.route('/')
def index():
    return render_template("index.html", name="Dominika")


@app.route('/url_parser/', methods=['POST'])
def form_post_endpoint():
    url = request.form['url']
    return redirect('/single_page_parser/' + url)

@app.route('/progress/<_id>')
def parsing_progress(_id):
    global parse_progress
    return {"status": parse_progress[_id].status, 'message': parse_progress[_id].status_message}

@app.route('/single_page_parser/<url>')
def single_page_parser(url):
    global parse_progress
    url_parser = ParserClass(url)
    parse_progress[url] = url_parser
    parse_progress[url].start()
    parse_progress[url].join()
    val_dict = url_parser.data
    return render_template("url_parser.html", values=val_dict)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

