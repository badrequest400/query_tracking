from flask import render_template, request, redirect, session, g, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, models, db, lm
from forms import Login

sql_text = '' 	# global var to store sql text between POST and GET cycle of
				# sql view (otherwise it gets overwritten at GET after JS has
				#	set the correct sql text from the db at POST)

@app.route('/index', methods=['POST', 'GET'])
@login_required
def index():
	# list of 'row' objects from the db
	queries = models.Query.query.all()

	#geting the distinct values for relevant fields
	#to build filtering functionality
	distinct_io = db.session.query(models.Query.total_io_count.distinct()).all()
	distinct_cpu = db.session.query(models.Query.total_cpu_time.distinct()).all()
	distinct_cpu_skew = db.session.query(models.Query.cpu_skew.distinct()).all()
	distinct_io_skew = db.session.query(models.Query.io_skew.distinct()).all()
	distinct_spool = db.session.query(models.Query.spool_usage.distinct()).all()
	distinct_pji = db.session.query(models.Query.pji.distinct()).all()
	distinct_uii = db.session.query(models.Query.uii.distinct()).all()

	if request.method == 'POST':

		#updating the status fields when choosing new value

		post = request.form.items()[0][0]

		clss = post[:post.find(",")]
		data = post[post.find(",")+1:]

		row_list = models.Query.query.filter(models.Query.id == clss).all()
		row = row_list[0]

		row.status = data
		db.session.commit()

		return redirect('/')


	return render_template("index.1.3.html", 
		queries = queries,
		distinct_io = distinct_io,
		distinct_cpu = distinct_cpu,
		distinct_cpu_skew = distinct_cpu_skew,
		distinct_io_skew = distinct_io_skew,
		distinct_spool = distinct_spool,
		distinct_pji = distinct_pji,
		distinct_uii = distinct_uii)

@app.route('/sql_text', methods=['POST', 'GET'])
@login_required
def sql():
	
	if request.method == 'POST':

		global sql_text

		clss = request.form.items()[0][0]

		row_list = models.Query.query.filter(models.Query.id == clss).all()
		row = row_list[0]

		sql_text = row.sql

		return redirect('/sql_text')

	return render_template("sql_text.html", sql_text = sql_text)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():

	if g.user != None and g.user.is_authenticated():
		return redirect('/index')

	form = Login()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data

		user = models.User.query.filter(models.User.username == form.username.data).first()
		if user == None:
			return redirect('/login')

		if form.password.data != user.password:
			return redirect('/login')

		remember_me = False
		if 'remember_me' in session:
			remember_me = session['remember_me']
			session.pop('remember_me', None)

		login_user(user, remember = remember_me)
		return redirect('/index')	

	return render_template("login.html", form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/index')

@app.route('/filter', methods = ['POST'])
def filter():
	post = request.form.items()

	name = post[0][0]
	data = post[0][1]

	return redirect(url_for('filter_results', name = name, data = data))

@app.route('/filter_results/<name>/<data>')
def filter_results(name, data):
	queries = db.session.query(models.Query).filter(getattr(models.Query, name) == data).all()

	distinct_io = db.session.query(models.Query.total_io_count.distinct()).all()
	distinct_cpu = db.session.query(models.Query.total_cpu_time.distinct()).all()
	distinct_cpu_skew = db.session.query(models.Query.cpu_skew.distinct()).all()
	distinct_io_skew = db.session.query(models.Query.io_skew.distinct()).all()
	distinct_spool = db.session.query(models.Query.spool_usage.distinct()).all()
	distinct_pji = db.session.query(models.Query.pji.distinct()).all()
	distinct_uii = db.session.query(models.Query.uii.distinct()).all()

	return render_template("index.1.3.html",
		queries = queries,	
		distinct_io = distinct_io,
		distinct_cpu = distinct_cpu,
		distinct_cpu_skew = distinct_cpu_skew,
		distinct_io_skew = distinct_io_skew,
		distinct_spool = distinct_spool,
		distinct_pji = distinct_pji,
		distinct_uii = distinct_uii)

@app.route('/order', methods = ['POST'])
def order():
	post = request.form.items()

	name = post[0][0]
	data = post[0][1]

	return redirect(url_for('order_results', name = name, data = data))

@app.route('/order_results/<name>/<data>')
def order_results(name, data):

	if data == 'desc':
		queries = db.session.query(models.Query).order_by(getattr(models.Query, name).desc()).all()
	else:
		queries = db.session.query(models.Query).order_by(getattr(models.Query, name).asc()).all()

	distinct_io = db.session.query(models.Query.total_io_count.distinct()).all()
	distinct_cpu = db.session.query(models.Query.total_cpu_time.distinct()).all()
	distinct_cpu_skew = db.session.query(models.Query.cpu_skew.distinct()).all()
	distinct_io_skew = db.session.query(models.Query.io_skew.distinct()).all()
	distinct_spool = db.session.query(models.Query.spool_usage.distinct()).all()
	distinct_pji = db.session.query(models.Query.pji.distinct()).all()
	distinct_uii = db.session.query(models.Query.uii.distinct()).all()

	return render_template("index.1.3.html",
		queries = queries,	
		distinct_io = distinct_io,
		distinct_cpu = distinct_cpu,
		distinct_cpu_skew = distinct_cpu_skew,
		distinct_io_skew = distinct_io_skew,
		distinct_spool = distinct_spool,
		distinct_pji = distinct_pji,
		distinct_uii = distinct_uii)

@lm.user_loader
def load_user(id):
	return models.User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user