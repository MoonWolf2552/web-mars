from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    id_ast = StringField('ID Астронавта', validators=[DataRequired()])
    passwd_ast = PasswordField('Пароль Астронавта', validators=[DataRequired()])
    id_cap = StringField('ID Капитана', validators=[DataRequired()])
    passwd_cap = PasswordField('Пароль Капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')