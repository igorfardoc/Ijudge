# -*- coding: utf8 -*-
import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Solution(SqlAlchemyBase):
    __tablename__ = 'solutions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    problem_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("problems.id"))
    status = sqlalchemy.Column(sqlalchemy.String)
    solution_file = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())