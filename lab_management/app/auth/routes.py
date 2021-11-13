from flask import render_template, flash, redirect, url_for, session, g, request, jsonify, make_response, send_from_directory, send_file, current_app

from app.header_imports import *

from app.auth import bp

from app.models import User

from app.forms import LoginForm



@bp.route('/login', methods=['GET','POST'])
def login():
    
	form = LoginForm()
 
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		user = User.query.filter_by(user_name=form.user_name.data).first()

		if user and user.password == form.password.data:
			login_user(user, form.remember_me.data)
			notice = ' Logged in as: %s ' % (current_user.user_name)
			user.online = True
			db.session.add(user)
			db.session.commit()
			flash(str(notice), category='success')
			return redirect(request.args.get('next') or url_for('home'))
		else: 
			flash('INCORRECT User Name OR Password', category='fail')



	return render_template('auth/login.html', form=form)



@bp.route('/logout')
@login_required
def logout():
	current_user.online = False
	db.session.add(current_user)
	db.session.commit()
	logout_user()
	# flash(' you have been logged out', category='warning')
	return redirect(url_for('auth.login'))