# -*- coding: utf8 -*-
import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Contest(SqlAlchemyBase):
    __tablename__ = 'contests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime)
    finish_date = sqlalchemy.Column(sqlalchemy.DateTime)
    problems = orm.relation("Problem",
                            secondary="association",
                            backref="contests")