from functools import wraps

from flask import redirect, url_for, flash, request
from flask_login import current_user


def admin_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.user and not current_user.admin:
            if current_user.confirmed:
                flash('You are not an admin', category='danger')
                return redirect(url_for('user.account', next=request.url))
            flash('You are not an admin', category='danger')
            return redirect(url_for('user.unconfirmed', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def normal_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin and not current_user.user:
            flash('You are not a user', category='danger')
            return redirect(url_for('admin.home', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def confirmed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            flash('Kindly confirm your account', category='warning')
            return redirect(url_for('user.unconfirmed', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def unconfirmed_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed:
            flash('Your account is already confirmed', category='info')
            return redirect(url_for('user.account', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def anonymous(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_anonymous:
            if current_user.user:
                flash('You are already logged in as: ' + current_user.email, category='info')
                return redirect(url_for('user.account', next=request.url))
            flash('You are already logged in: ' + current_user.email, category='info')
            return redirect(url_for('admin.home', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
