import os
import markdown
from flask import render_template, send_from_directory, Markup
from poptraq import app


@app.route('/', methods=['GET'])
def index():
        return render_template('index.html')


@app.route('/about', methods=['GET'])
def about():
    with open("./docs/README.md") as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('about.html', content=content)


@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, './static/img'), 'favicon.ico')
