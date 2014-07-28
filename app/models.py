from app import db

USER_ROLE = 0
ADMIN_ROLE = 1

class Query(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	proc_id = db.Column(db.String(120))
	query_id = db.Column(db.String(120))
	user_name = db.Column(db.String(120), index = True)
	session_id = db.Column(db.String(120))
	app_id = db.Column(db.String(120))
	client_id = db.Column(db.String(120))
	last_resp_time = db.Column(db.String(120))
	elapsed_time = db.Column(db.String(120))
	delay_in_minutes = db.Column(db.String(120))
	num_steps = db.Column(db.String(120))
	total_io_count = db.Column(db.Float(precision=12), index = True)
	total_cpu_time = db.Column(db.Float(precision=12), index = True)
	cpu_skew = db.Column(db.Float(precision=12))
	io_skew = db.Column(db.Float(precision=12))
	spool_usage = db.Column(db.Float(precision=12))
	pji = db.Column(db.Float(precision=12))
	uii = db.Column(db.Float(precision=12))
	sql = db.Column(db.String(10000))
	status = db.Column(db.String(20))
	assigned = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return 'Query: %d' % (self.id)

class User(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50))
	password = db.Column(db.String(50))
	role = db.Column(db.Integer, default = USER_ROLE)
	assignedTo = db.relationship('Query', backref = 'owner', lazy = 'dynamic')

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return 'Username: %s' % (self.username)
