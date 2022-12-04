from flask import Blueprint, render_template, redirect, flash, url_for
from .forms import UserRegisterForm, UserLoginForm
from .models import UserModel
from src.extensions import db
from flask_login import login_user, logout_user


accounts = Blueprint('accounts', __name__,
                     template_folder='templates',
                     static_folder='static')


@accounts.route('/signup', methods=['GET', 'POST'])
def register_user():
    form = UserRegisterForm()
    username = form.username.data
    password1 = form.password1.data
    password2 = form.password2.data
    if form.validate_on_submit():
        user = UserModel(username=username, password=password1)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('notes.notes_list'))
    else:
        flash(form.errors, category='danger')
    return render_template('accounts/register_page.html', form=form)


@accounts.route('/signin', methods=['GET', 'POST'])
def signin_user():
    form = UserLoginForm()
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('notes.notes_list'))
        else:
            flash('Неправильные имя пользователя или пароль. Попробуйте снова', category='danger')
    return render_template('accounts/login_page.html', form=form)


@accounts.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('accounts.signin_user'))


