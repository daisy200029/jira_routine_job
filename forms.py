from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, SelectField, PasswordField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class ContactForm(Form):
  jira_name = TextField("JIRA Name",  [validators.Required("Please enter your jira name.")])
  jira_password = PasswordField("JIRA Password",  [validators.Required("Please enter your jira password.")])
  upload = FileField('upload', validators=[validators.Required("Please choose a file."), FileAllowed(['txt'], 'Please upload .txt file')])  
  submit = SubmitField("Start!")
  select_type = SelectField("Post Type", choices=[('test_step','Test Steps'),('bug','Bugs')])


