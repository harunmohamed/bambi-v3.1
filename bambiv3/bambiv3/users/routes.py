from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from bambiv3 import db, bcrypt
from bambiv3.models import User, Post
from bambiv3.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from bambiv3.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, department=form.department.data,\
			student_number=form.student_number.data, age=form.age.data, country=form.country.data, hobby=form.hobby.data,\
			password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Account Created for {form.username.data}! You can now log in', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title="Register", form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash(f'Login Unsuccesful! Please try again.', 'danger')
	return render_template('login.html', title="Login", form=form)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.department = form.department.data
		current_user.student_number = form.student_number.data
		current_user.country = form.country.data
		current_user.age = form.age.data
		current_user.hobby = form.hobby.data
		db.session.commit()
		flash('Your Account has been updated', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.department.data = current_user.department
		form.student_number.data = current_user.student_number
		form.country.data = current_user.country
		form.age.data = current_user.age
		form.hobby.data = current_user.hobby
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)



@users.route("/user/<string:username>", methods=['GET', 'POST'])
def user_posts(username):
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.department = form.department.data
		current_user.student_number = form.student_number.data
		current_user.country = form.country.data
		current_user.age = form.age.data
		current_user.hobby = form.hobby.data
		db.session.commit()
		flash('Your Account has been updated', 'success')
		return redirect(url_for('users.user_posts', username=current_user.username))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.department.data = current_user.department
		form.student_number.data = current_user.student_number
		form.country.data = current_user.country
		form.age.data = current_user.age
		form.hobby.data = current_user.hobby
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('user_posts.html', posts=posts, user=user, title=user.username,image_file=image_file,form=form)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been set with instructions to reset your password','info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'danger')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

