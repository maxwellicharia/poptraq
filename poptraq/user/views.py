from flask import render_template, request, url_for, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from poptraq.form import Signup, Login
from poptraq.models import User
from poptraq import user, db


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signup(request.form)  # instantiating form to use the forms defined from the Form class in form.py

    if request.method == 'GET':
        return render_template('signup.html', form=form)
    else:
        if not form.validate_on_submit():  # making sure that the form is validated before submission
            return render_template('signup.html', form=form, not_validate=True)
        else:
            password = request.form['password']
            pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            new_user = User(request.form['national_id'],
                            request.form['first_name'],
                            request.form['surname'],
                            request.form['dob'],
                            request.form['home_county'],
                            request.form['email'],
                            pw_hash)
            db.session.add(new_user)
            db.session.commit()
            session['logged_in'] = True
            return redirect(url_for('account'))


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(request.form)  # instantiating form to use the forms defined from the Form class in form.py

    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        if not form.validate_on_submit():  # making sure that the form is validated before submission
            return render_template('login.html', form=form, not_validate=True)
        else:
            national_id = request.form['national_id']
            email = request.form['email'],
            password = request.form['password']
            exists = User.query.filter_by(
                    national_id=national_id).first()
            if (email != exists.email) and (check_password_hash(exists.password, password) is False):
                return redirect(url_for('login'))
            else:
                return redirect(url_for('account'))


@user.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('dash'))


@user.route('/account', methods=['GET', 'POST'])
def account(id_no):
    id_no = signup.national_id
    return render_template('account.html', **locals())
