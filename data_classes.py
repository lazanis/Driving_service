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


class Offer(Base):
    __tablename__ = 'OFFERS'
    id = sql.Column(sql.String, primary_key=True, default=uuid4)
    drive_from = sql.Column(sql.String)
    drive_to = sql.Column(sql.String)
    drive_date = sql.Column(sql.BIGINT)
    user_id = sql.Column(sql.String, sql.ForeignKey('USERS.id', ondelete='CASCADE'), nullable=False)
    request_type = sql.Column(sql.String)
    car_id = sql.Column(sql.String, sql.ForeignKey('CARS.id', ondelete='CASCADE'), nullable=False)


class Drive(Base):
    __tablename__ = 'DRIVES'
    id = sql.Column(sql.String, primary_key=True, default=uuid4)
    offer_id = sql.Column(sql.String, sql.ForeignKey('OFFERS.id', ondelete='CASCADE'), nullable=False)
    passenger_id = sql.Column(sql.String, sql.ForeignKey('USERS.id', ondelete='CASCADE'), nullable=False)
    reservation_date = sql.Column(sql.BIGINT)


class Review(Base):
    __tablename__ = 'REVIEWS'
    id = sql.Column(sql.String, primary_key=True, default=uuid4)
    from_user_id = sql.Column(sql.String, sql.ForeignKey('USERS.id', ondelete='CASCADE'), nullable=False)
    to_user_id = sql.Column(sql.String, sql.ForeignKey('USERS.id', ondelete='CASCADE'), nullable=False)
    drive_id = sql.Column(sql.String, sql.ForeignKey('DRIVES.id', ondelete='CASCADE'), nullable=False)
    review_date = sql.Column(sql.BIGINT)
    review_grade = sql.Column(sql.INT)
