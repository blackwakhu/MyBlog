from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, TextAreaField, EmailField
from wtforms.validators import DataRequired, InputRequired


class Form1(FlaskForm):
    author = StringField("Author", validators=[DataRequired(), InputRequired()])
    username = StringField("Username", validators=[DataRequired(), InputRequired()])
    passwd = PasswordField("Password", validators=[DataRequired(), InputRequired()])
    security_question = StringField("Security Question", validators=[DataRequired(), InputRequired()])
    answer = StringField("Answer", validators=[DataRequired(), InputRequired()])
    title = StringField("Title", validators=[DataRequired(), InputRequired()])
    content = TextAreaField("Content", validators=[DataRequired(), InputRequired()])
    subject = StringField("Subject", validators=[DataRequired(), InputRequired()])
    email = EmailField("Author email")
    submit = SubmitField("save")

