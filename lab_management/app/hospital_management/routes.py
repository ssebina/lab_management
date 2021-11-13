from app.hospital_management import bp

from app.models import Hospital, User, Permission

@bp.context_processor
def system_permissions():
	return dict(Permission = Permission)



from app.header_imports import *


@bp.route('/new_hospital', methods=['GET', 'POST'])
def new_hospital():

	if request.method == 'POST':

		if 'one' == request.get_json()['step']:

			return jsonify({'resp': render_template('hospital_management/new_hospital_steps/step_1.html')})

		if 'one-two' == request.get_json()['step']:

			return jsonify({'resp':Hospital.add(request.get_json())})

		if 'admin-options' == request.get_json()['step']:

			admin_list = []

			for u in User.query.all():
				admin_list.append(u.user_name)

			return jsonify({'admins_list': admin_list})
	

	return render_template('hospital_management/new_hospital.html')