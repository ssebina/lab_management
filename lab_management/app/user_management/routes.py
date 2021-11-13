from app.header_imports import *

from app.user_management import bp

from app.models import User, Permission

@bp.context_processor
def system_permissions():
	return dict(Permission = Permission)




@bp.route('/new_user', methods=['POST','GET'])
def new_user():


	if request.method == 'POST':
		data = request.get_json()

		if data['step'] == 'one':
			return jsonify({'resp':render_template('user_management/new_user_steps/step_1.html')})

		if data['step'] == 'one-two':
			return jsonify({'resp': User.add(data)})

	return render_template('user_management/new_user.html')