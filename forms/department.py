from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, EmailField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    chief = SelectField('Шеф', coerce=int, validators=[DataRequired()])
    members = StringField('Список id участников', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class EdDepartmentForm(DepartmentForm):
    submit = SubmitField('Сохранить')
