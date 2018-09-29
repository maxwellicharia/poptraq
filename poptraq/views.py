import os
import markdown
from flask import render_template, send_from_directory, Markup
from poptraq import app


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    with open("./docs/README.md") as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('about.html', **locals())


@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(index.root_path, './static/img'), 'favicon.ico')
