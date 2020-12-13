from flask import render_template, url_for, flash, redirect
from subwaymapper import app
from subwaymapper.forms import RegistrationForm, LoginForm
from subwaymapper.models import *
from subwaymapper.service import *
from subwaymapper.repository import *
from flask_login import login_user, current_user, logout_user, login_required
from flask import request

user_service = UserService()
schedule_service = ScheduleService()
i = 0

@app.route('/')
def home():
	x = schedule_service.get_schedules_by_line("Trains/1")
	#x = schedule_service.get_schedules_by_line_as_dict("Trains/1")
	#names = x[0].keys()
	#print(x[0].line)
	return render_template('home.html', title='Home', crown=x)

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		if user_service.confirm_unique_email(form.email.data):
			user_service.add_user(++i, form.email.data, form.password.data, 0)
			flash('Your account has been created! You are now able to log in', 'success')
			return redirect(url_for('login'))
		else:
			flash('This email is already registered, please log in or choose a different email', 'danger')
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		x = user_service.confirm_unique_email(form.email.data)
		if x == False:
			if user_service.login_user(form.email.data,form.password.data):
				flash('You have been logged in!', 'success')
				user = user_service.get_actual_user_by_email(form.email.data)
				login_user(user, remember = form.remember.data)
				next_page = request.args.get('next')
				return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/trains")
def trains():
	return render_template('about.html', title='About')

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
	return render_template('account.html', title='Account')

@app.route("/about")
def about():
	return render_template('about.html', title='About')
