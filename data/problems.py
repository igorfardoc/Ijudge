# -*- coding: utf8 -*-
import sqlalchemy
from .db_session import SqlAlchemyBase


association_table = sqlalchemy.Table('association', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('contests', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('contests.id')),
                                     sqlalchemy.Column('problems', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('problems.id')))


class Problem(SqlAlchemyBase):
    __tablename__ = 'problems'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    task_file = sqlalchemy.Column(sqlalchemy.String)
    tests_file = sqlalchemy.Column(sqlalchemy.String)
    answers_file = sqlalchemy.Column(sqlalchemy.String)
    time_limit = sqlalchemy.Column(sqlalchemy.Integer)
    file_in = sqlalchemy.Column(sqlalchemy.String)
    file_out = sqlalchemy.Column(sqlalchemy.String)