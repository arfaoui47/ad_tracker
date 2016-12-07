from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import User


class SignupForm(Form):
    firstname = TextField(
        "First name", [validators.Required("Please enter your first name.")])
    lastname = TextField(
        "Last name", [validators.Required("Please enter your last name.")])
    email = TextField("Email", [validators.Required(
        "Please enter your email address."), validators.Email(
        "Please enter your email address.")])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            print 's'
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        print user
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class SigninForm(Form):
    email = TextField("Email", [validators.Required(
        "Please enter your email address."), validators.Email(
        "Please enter your email address.")])
    password = PasswordField(
        'Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")
    firstname = ''

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            self.firstname = user.firstname.encode('utf-8')
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[validators.Required()]
    )
