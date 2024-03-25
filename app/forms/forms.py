from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileAllowed
from wtforms_sqlalchemy.fields import QuerySelectMultipleField


class PasswordValidator:
    def __init__(self, message = None):
        if message is None:
            message = 'Password must contain at least one digit, one special character, and consist only of Latin letters.'
        self.message = message

    def __call__(self, form, field):
        password = field.data
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one digit.')
        if not any(char in '!@#$%^&*()[]{}?/\|~' for char in password):
            raise ValidationError('Password must contain at least one special character.')
        # if not password.isascii():
        #     raise ValidationError('Password must consist only of Latin letters.')


def get_themes():
    from app.models import Theme
    return Theme.query.all()


class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    description = StringField('Description', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    themes = QuerySelectMultipleField('Themes', query_factory=lambda:get_themes(), get_label="name")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=50)])
    submit = SubmitField('Login')


class SingUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50), PasswordValidator()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sing Up')
