import os
import markdown
from flask import render_template, send_from_directory, Markup, session
from poptraq import app


@app.route('/', methods=['GET'])
def index():
    if session.get('email') is None:
        return render_template('index.html')
    else:
        email = session['email']
        return render_template('index.html', email=email)


@app.route('/about', methods=['GET'])
def about():
    if session.get('email') is None:
        with open("./docs/README.md") as f:
            content = f.read()
        content = Markup(markdown.markdown(content))
        return render_template('about.html', content=content)
    else:
        email = session['email']
        with open("./docs/README.md") as f:
            content = f.read()
        content = Markup(markdown.markdown(content))
        return render_template('about.html', **locals())


@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, './static/img'), 'favicon.ico')
