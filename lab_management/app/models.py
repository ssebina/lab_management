from app import db
from flask_login import UserMixin
# from datetime import datetime
import datetime 

from sqlalchemy import desc

from flask_login import current_user



#  THIS IS USER PERMISSIONS

class Permission:
	CAN_COMMENT = 0B00000001
	CAN_ENDOSE = 0B00000010
	CAN_CHANGE_STATE = 0B00000100
	CAN_VIEW_ALL = 0B00001000
	CAN_RECORD_NEW_HOSPITAL = 0B00010000
	CAN_RECORD_NEW_USER = 0B00100000
	CAN_RECORD_NEW_EQUIPMENT = 0B01000000


######################################################## USER REGISTRATION ##########################################


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(128))
	contact = db.Column(db.String(130))
	user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.id'))

	complaints = db.relationship('Complaint', backref='endosor', lazy='dynamic')
	comments = db.relationship('Comment', backref='author', lazy='dynamic')
	hospital = db.relationship('Hospital', backref='admin', uselist=False)

	actions = db.relationship('Action', backref='author', lazy='dynamic')
	
	def has_permission(self, permission):
    		return self.user_type is not None and (self.user_type.permissions & permission) == permission
 
	def is_system_admin(self):
		return self.has_permission(0xFF)

	def user_type_name(self):
		return self.user_type.name

	def __repr__(self):
		return '<User %r>' % (self.user_name)


	@staticmethod
	def add(data):
		u = User.query.filter_by(user_name=data['username']).first()

		if u is None:
			u = User()
			u.user_name = data['username']
			u.password = data['password']
			u.contact = data['contact']

			db.session.add(u)
			db.session.commit()

			return 'Operation Successful'
		else:
		 	return 'Username Already Exists'




class UserType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	users = db.relationship('User', backref='user_type', lazy='dynamic')
	permissions = db.Column(db.Integer)

	@staticmethod
	def update_types():

		roles = {
			'TECHNICIAN': Permission.CAN_COMMENT | Permission.CAN_CHANGE_STATE ,
			'SUPERIOR_OBSERVER': Permission.CAN_VIEW_ALL | Permission.CAN_COMMENT,
			'HOSPITAL_ADIMN' : Permission.CAN_COMMENT | Permission.CAN_ENDOSE | Permission.CAN_RECORD_NEW_EQUIPMENT,
			'SYSTEM_ADMIN' : 0xFF
		}

		for r in roles:
			_role_ = UserType.query.filter_by(name=r).first()

			if _role_ is None:
				_role_ = UserType(name=r)
			_role_.permissions = roles[r]  

			db.session.add(_role_)
			print("done ---> [ {} ]".format(r))	

		db.session.commit()		
		print("Done Adding all...")



class Equipment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	department = db.Column(db.String(64))
	model = db.Column(db.String(64))
	serial_no = db.Column(db.String(100))
	room_no = db.Column(db.String(20))
	sticker_info = db.Column(db.String(20))
	hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
	complaints = db.relationship("Complaint", backref="equipment", lazy="dynamic")

	@staticmethod
	def add(data):

		hospital = Hospital.query.filter_by(name=data['hospital_name'].strip()).first()

		if hospital is not None:

			eq = Equipment()
			eq.name = data['equipment_name']
			eq.department = data['department_name']
			eq.model = data['machine_model']
			eq.serial_no = data['serial_number']
			eq.room_no = data['room_number']
			eq.sticker_info = data['sticker_information']
			eq.hospital = hospital

			db.session.add(eq)
			db.session.commit()

			return 'Operation Successful: New Equipment Added'

		else:
			return 'Operation Failed Hospital Does not Exists in the System'



class Complaint(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	date = db.Column(db.DateTime, index=True)
	equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
	endosor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	narrative  = db.Column(db.String(250))
	actions = db.relationship('Action', backref='complaint', lazy='dynamic')
	deleted = db.Column(db.Boolean, default=False)
	comments = db.relationship('Comment', backref='complaint', lazy='dynamic')

	def recent_action(self):

		if self.actions.count():
			return  self.actions.order_by(desc(Action.id)).first().action_type

		else:
			return 'PENDING...'

	@staticmethod
	def add(data):
		comp = Complaint()
		comp.date = datetime.datetime.now()
		comp.equipment_id = int(data['equipment_id'])
		comp.narrative = data['narrative']
		comp.endosor = current_user

		db.session.add(comp)
		db.session.commit()

		return "Operation Successful New Complaint Recorded"



class Comment(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	date = db.Column(db.DateTime, index=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	narrative = db.Column(db.String(200))
	complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'))

	@staticmethod
	def add(data):
		comment  = Comment()
		comment.date = datetime.datetime.now()
		comment.narrative = data['narrative']
		comment.complaint_id = data['complaint_id']
		comment.author_id = current_user.id

		db.session.add(comment)
		db.session.commit()

		return "New Comment Added"



class Action(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, index=True)
	action_type = db.Column(db.String(20))
	narrative = db.Column(db.String(200))
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'))

	@staticmethod
	def add(data):
		act = Action()
		act.date = datetime.datetime.now()
		act.author_id = current_user.id
		act.narrative = data['narrative']
		act.action_type = data['action_type']
		act.complaint_id = data['complaint_id']

		db.session.add(act)
		db.session.commit()

		return "Successful"



class Hospital(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	reg_date = db.Column(db.DateTime, index=True)
	name = db.Column(db.String(30))
	admin_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
	address = db.Column(db.String(100))
	equipment_list = db.relationship('Equipment', backref='hospital', lazy='dynamic')

	@staticmethod
	def add(data):

		admin = User.query.filter_by(user_name=data['admin_name'].strip()).first()

		if admin is not None:

			if Hospital.query.filter_by(name=data['hospital_name'].strip()).first() is None:

				hosp = Hospital()
				hosp.reg_date = datetime.datetime.now()
				hosp.name = data['hospital_name'].strip()
				hosp.address = data['hospital_location'].strip()
				hosp.admin_id = admin.id

				db.session.add(hosp)
				db.session.commit()

				return 'Operation Successful: New Hospital Added to System'

			else:
				return 'Operation Failed : Hospital Already Exists'
				
		else:
			return "Operation Failed : Admin User not Recognised"