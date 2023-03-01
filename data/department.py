import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    __tablename__ = 'department'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # шеф
    members  = sqlalchemy.Column(sqlalchemy.ARRAY, nullable=True)  # члены
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)  # элекорнная почта
    user = orm.relationship('User')