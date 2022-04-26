from app.equipment_management import bp

from app.header_imports import *

from sqlalchemy import desc

from app.models import Hospital, Equipment, Complaint, Comment, Action, Permission



@bp.context_processor
def system_permissions():
	return dict(Permission = Permission)

@bp.route('new_equipment', methods=['POST', 'GET'])
@login_required
def new_equipment():


	if request.method  == 'POST':

		if 'one' == request.get_json()['step']:

			return jsonify({'resp': render_template('equipment_management/new_equipment_steps/step_1.html')})

		if 'one-two' == request.get_json()['step']:

			return jsonify({'resp': Equipment.add(request.get_json())})

		if 'hospital_list' == request.get_json()['step']:

			hospital_list = []

			for hosp in Hospital.query.all():
				hospital_list.append(hosp.name)

			return jsonify({'hospitals':hospital_list})


	return  render_template('equipment_management/new_equipment.html')




@bp.route('equipment_list', methods=['POST', 'GET'])
@login_required
def equipment_list():


	if request.method == 'POST':

		if 'equipment_table' == request.get_json()['step']:
			return jsonify({'table': render_template('equipment_management/equipment_list_files/equipment_list_table.html',
							equipment = Equipment.query.all())})

		if 'equipment_details' == request.get_json()['step']:
			return jsonify({'details' : render_template('equipment_management/equipment_list_files/equipment_details.html',
							equipment = Equipment.query.get(int(request.get_json()['equipment_id'])))})

		if 'new_complaint' == request.get_json()['step']:
			return jsonify({'resp' : Complaint.add(data=request.get_json())})


	return render_template('equipment_management/equipment_list_files/equipment_list.html')




@bp.route('complaint_view', methods=['POST', 'GET'])
@login_required
def complaint_view():


	all_complaints=Complaint.query.order_by(desc(Complaint.id)).all()

	return render_template('equipment_management/complaints/complaints_view.html',
							all_complaints=all_complaints)



@bp.route('/get_comments', methods=['POST'])
@login_required
def get_comments():


	comments_list = []

	comments_view = ''

	complaint = Complaint.query.get(int(request.get_json()['complaint_id']))

	count = complaint.comments.count()

	if count > 0:

		msg = 'OKAY'

		for com in complaint.comments:
			comment = {}

			comment.update(comment = com.narrative)

			comment.update(author = com.author.user_name)

			comments_list.append(comment)

		comments_view = render_template('equipment_management/complaints/comments_view.html', comments=comments_list)


	else :
		msg = "NO AVAILABLE COMMENTS"


	return jsonify({'comments': comments_view , 'count': count, 'msg': msg})






@bp.route('/post_comment', methods=['POST'])
@login_required
def post_commnet():


	return jsonify({'resp':Comment.add(request.get_json())})


@bp.route('add_complaint_action', methods=['POST'])
@login_required
def add_complaint_action():

	return jsonify({'response': Action.add(request.get_json())})


@bp.route('get_actions_list', methods=['POST'])
@login_required
def get_actions_list():

	actions_list = Complaint.query.get(request.get_json()['complaint_id']).actions

	if not actions_list.count():
		return jsonify({'response': 'No actions taken so far'})

	return jsonify({'response': render_template('equipment_management/complaints/actions_view.html', actions=actions_list)})