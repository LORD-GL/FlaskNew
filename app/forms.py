from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileAllowed
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from app.models import Theme


class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    description = StringField('Description', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    themes = QuerySelectMultipleField('Themes', query_factory=lambda: Theme.query.all(), get_label="name")

