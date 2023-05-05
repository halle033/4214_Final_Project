from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired



class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

	submit = SubmitField('Sign In')

class CryptoClassForm(FlaskForm):
	crypto_class_name = StringField('Crypto Class Name', validators=[DataRequired()])
	crypto_percent = StringField('Crypto Percent', validators=[DataRequired()])
	submit = SubmitField('Update')

############ CRYPTOS ############
class CryptoForm(FlaskForm):
	crypto_symbol = StringField('Crypto Symbol', validators=[DataRequired()])
	company_name = StringField('Company Name', validators=[DataRequired()])
	crypto_class = SelectField('Crypto Class', choices=[])
	submit = SubmitField()