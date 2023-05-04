from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired



class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

	submit = SubmitField('Sign In')

class AssetClassForm(FlaskForm):
	asset_class_name = StringField('Asset Class Name', validators=[DataRequired()])
	allocation_percent = StringField('Allocation Percent', validators=[DataRequired()])
	submit = SubmitField('Update')

############ TICKERS ############
class TickerForm(FlaskForm):
	ticker_symbol = StringField('Ticker Symbol', validators=[DataRequired()])
	company_name = StringField('Company Name', validators=[DataRequired()])
	asset_class = SelectField('Asset Class', choices=[])
	submit = SubmitField()