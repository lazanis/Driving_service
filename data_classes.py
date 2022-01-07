from uuid import uuid4
import sqlalchemy as sql
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'USERS'
    id = sql.Column(sql.String, primary_key=True, default=uuid4)
    name = sql.Column(sql.String)
    surname = sql.Column(sql.String)
    role = sql.Column(sql.String)
    date_of_birth = sql.Column(sql.BIGINT)
    username = sql.Column(sql.String)
    pwd = sql.Column(sql.String)
    email = sql.Column(sql.String)


class Car(Base):
    __tablename__ = 'CARS'
    id = sql.Column(sql.String, primary_key=True, default=uuid4)
    user_id = sql.Column(sql.String, sql.ForeignKey('USERS.id', ondelete='CASCADE'), nullable=False)
    seats = sql.Column(sql.INT)
    type = sql.Column(sql.String)
