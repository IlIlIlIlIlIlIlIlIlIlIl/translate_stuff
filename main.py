# import argparse
from flask import Flask, render_template, request, redirect, url_for
from parser_class import ParserClass

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html", name="Dominika")


@app.route('/url_parser/', methods=['POST'])
def form_post():
    url = request.form['url']
    return redirect('/single_page_parser/' + url)


@app.route('/single_page_parser/<url>')
def hello_name(url):
    url_parser = ParserClass(url)
    val_dict = url_parser.stats
    return render_template("url_parser.html", values=val_dict)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Process webpages.')
    # parser.add_argument('--url', help='Link to webpage')
    # args = parser.parse_args()
    #
    # my_parser = ParserClass(args.url)
    app.run(host='127.0.0.1', port=8080, debug=True)

