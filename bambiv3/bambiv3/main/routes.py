from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from bambiv3.models import Post, User
from bambiv3 import db, bcrypt, mail
from bambiv3.posts.forms import PostForm
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your Post Has been Created!', 'success')
		return redirect(url_for('main.home'))
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
	users = User.query.all()
	if current_user.is_authenticated:
		image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
		return render_template('home.html', title="Home", form=form, posts=posts, image_file=image_file, users=users)
	else:
		return redirect(url_for('users.login'))
		#return render_template('home.html', title="Home", posts=posts)


@main.route('/about')
def about():
	return render_template('about.html', title="About")

@main.route('/market')
def market():
	return render_template('market.html', title="Market")

@main.route('/inbox')
def inbox():
	return render_template('inbox.html', title="Inbox")

@main.route('/discover')
def discover():
	users = User.query.all()
	return render_template('discover.html', users=users)

@main.route('/explore')
def explore():
	return render_template('explore.html', title="Explore")

#Error Handlers
@main.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main.errorhandler(403)
def forbidden_route_error(error):
    return render_template('403.html'), 403

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500