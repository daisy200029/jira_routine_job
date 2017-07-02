from flask import Flask, render_template, request, flash, send_from_directory, redirect,  url_for, session
from forms import ContactForm
from werkzeug import secure_filename
from bug_parser import bug_parser
from step_parser import step_parser
from jira_routine_job import  jira_routine
import os

app = Flask(__name__)
app.secret_key = 'development key'


def upload_and_save_file(form):
	f = form.upload.data
	filename = secure_filename(f.filename)
	file_path=os.path.join(
	os.path.dirname(os.path.abspath(__file__)), 'uploads', filename)
	f.save(file_path)
	return file_path



@app.route('/test_step_suceess')
def test_step_suceess():
    return render_template('home.html', success=True , tickets_id=session['tickets_id'])

@app.route('/bug_success')
def bug_suceess():
    return render_template('home.html', success=True , tickets_id=session['tickets_id'])


@app.route('/', methods=['GET', 'POST'])
def uploadfile():
	form = ContactForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			file_path=upload_and_save_file(form)
			try:
				routine=jira_routine(form.jira_name.data,form.jira_password.data)
				print "authentication success"
			except Exception as e:
				return "authentication fail"
			else:
				if form.select_type.data == 'bug':
					try:
						parser=bug_parser(file_path)	
					except Exception as e:
						return render_template('home.html', form=form, bugsizeError=True)
					else:
						try:
							tickets_id=routine.create_bug(assignee=parser.bug_assignee, summary=parser.bug_summary,description=parser.bug_des)
						except Exception as e:
							return render_template('home.html', form=form, AssigneeTypeError=True)
						else:
							session['tickets_id'] = tickets_id
							return  redirect(url_for('bug_suceess'))
				if form.select_type.data == 'test_step':
					try:			
						parser=step_parser(file_path)
					except Exception as e:
						return render_template('home.html', form=form, stepsizeError=True)
					else:
						try:
							tickets_id=routine.post_zephyr_teststep(ticket=parser.test_tickets,test_step=parser.test_step,test_data=parser.test_data,test_result=parser.test_result)
						except Exception as e:
							return render_template('home.html', form=form, ticketTypeError=True)
						else:
							session['tickets_id'] = tickets_id
							return  redirect(url_for('test_step_suceess'))
		else:
			flash('All fields are required.')
			return render_template('home.html', form=form)				
			
	elif request.method == 'GET':
		return render_template('home.html', form=form)

@app.route('/downloadBugExample', methods=['GET'])
def downloadBugExample():
	return  send_from_directory(".","bug.txt",as_attachment=True)
@app.route('/downloadStepExample', methods=['GET'])
def downloadStepExample():
	return  send_from_directory(".","step.txt",as_attachment=True)



if __name__ == '__main__':
  app.run(debug=True)
