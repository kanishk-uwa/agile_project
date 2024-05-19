from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

# Form for user login
class LoginForm(FlaskForm):
    # Username field, required
    username = StringField('Username', validators=[DataRequired()])
    # Password field, required
    password = PasswordField('Password', validators=[DataRequired()])
    # Submit button
    submit = SubmitField('Login')

# Form for user registration
class RegistrationForm(FlaskForm):
    # Username field, required, with length constraints
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=20)
    ])
    # Password field, required, with length constraints
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=30)
    ])
    # Confirm password field, required, must match password field
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')
    ])
    # Submit button
    submit = SubmitField('Register')

    # Custom validator to check if username is already taken
    def validate_username(self, username):
        from .models import User
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')
