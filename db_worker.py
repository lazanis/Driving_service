import base64
import pandas as pd
from uuid import uuid4
import sqlalchemy as sql
from datetime import datetime
from typing import Dict, Union
from sqlalchemy import select, and_
from sqlalchemy.orm import sessionmaker
from data_classes import User, Car, Offer, Drive


class DBWorker(object):
    def __init__(self, address: str = 'localhost', port: int = 3306, username: str = 'lazar', password: str = 'nissatech.20', database: str = 'Driving_service_db'):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection_str = f'mysql://{self.username}:{self.password}@{self.address}:{self.port}/{self.database}'

    # region User
    def check_if_user_exists_by_username(self, username: str):
        return_val = None
        try:
            engine = sql.create_engine(self.connection_str)
            Session = sessionmaker(bind=engine)
            session = Session()

            query = select(User).where(User.username == username)
            rez = session.execute(query)
            users = rez.scalars().all()
            no_rows = len(users)
            if no_rows == 1:
                return_val = users[0].id

            session.close()
        except Exception as e:
            print(f'Checking if user exists by username failed with error: {e}')
        finally:
            return return_val

    def check_if_user_exists_by_username_and_pwd(self, username: str, pwd: str):
        return_val = None
        return_role = None
        try:
            engine = sql.create_engine(self.connection_str)
            Session = sessionmaker(bind=engine)
            session = Session()
            pwd_search = pwd.encode('utf-8')
            pwd_search = base64.b64encode(pwd_search)

            query = select(User).where(and_(User.username == username, User.pwd == pwd_search))
            rez = session.execute(query)
            users = rez.scalars().all()
            no_rows = len(users)
            if no_rows == 1:
                return_val = users[0].id
                return_role = users[0].role

            session.close()
        except Exception as e:
            print(f'Checking if user exists by username failed with error: {e}')
        finally:
            return return_val, return_role

    def write_new_user(self, user_dict: Dict[str, Union[int, str, bytes]]):
        return_val = None
        return_message = 'success'
        try:
            new_id = str(uuid4())
            user_pwd = user_dict.get('pwd')
            user_pwd = user_pwd.encode('utf-8')
            user_pwd = base64.b64encode(user_pwd)
            user_dob = int(user_dict['date_of_birth'])
            new_user = User()
            new_user.id = new_id
            new_user.name = user_dict.get('name')
            new_user.surname = user_dict.get('surname')
            new_user.role = user_dict.get('role')
            new_user.date_of_birth = user_dob
            new_user.username = user_dict.get('username')
            new_user.pwd = user_pwd
            new_user.email = user_dict.get('email')

            engine = sql.create_engine(self.connection_str)
            Session = sessionmaker(bind=engine)
            session = Session()

            session.add(new_user)
            session.commit()

            session.close()

            return_val = new_id
        except Exception as e:
            print(f'Checking if user exists by username failed with error: {e}')
            return_message = f'error: {e}'
        finally:
            return return_val, return_message

    def get_all_users(self):
        # TODO: COMPLETE
        engine = sql.create_engine(self.connection_str)
        Session = sessionmaker(bind=engine)
        session = Session()

        query = select(User)
        rez = session.execute(query)
        users = rez.scalars().all()
        for u in users:
            print(u)

        session.close()
    # endregion

    # region Car
    def write_new_car(self, car_arguments: Dict[str, Union[str, int]]):
        return_val = None
        return_message = 'success'
        try:
            new_id = str(uuid4())
            new_car = Car()
            new_car.id = new_id
            new_car.user_id = car_arguments.get('user_id')
            new_car.seats = car_arguments.get('seats')
            new_car.type = car_arguments.get('type')

            engine = sql.create_engine(self.connection_str)
            Session = sessionmaker(bind=engine)
            session = Session()

            session.add(new_car)
            session.commit()

            session.close()

            return_val = new_id
        except Exception as e:
            print(f"New car addition for user {car_arguments.get('user_id')} failed with error: {e}")
            return_message = f'error: {e}'
        finally:
            return return_val, return_message

    def get_all_cars_for_user(self, user_id: str):
        return_val = None
        try:
            engine = sql.create_engine(self.connection_str)
            Session = sessionmaker(bind=engine)
            session = Session()

            query = select(Car).where(Car.user_id == user_id)
            rez = session.execute(query)
            cars = rez.scalars().all()
            return_val = cars

            session.close()
        except Exception as e:
            print(f'While obtaining cars for user {user_id} following error occurred: {e}')
        finally:
            return return_val
    # endregion

    # region Offer
    def add_new_offer(self, offer_args: Dict[str, Union[str, int]]):
        return_val = None
        return_message = 'success'
        try:
            new_id = str(uuid4())
            new_offer = Offer()
            new_offer.id = new_id
            new_offer.drive_from = offer_args.get('drive_from')
            new_offer.drive_to = offer_args.get('drive_to')
            new_offer.drive_date = int(offer_args.get('drive_date'))
            new_offer.user_id = offer_args.get('user_id')
            new_offer.request_type = offer_args.get('request_type')
            new_offer.car_id = offer_args.get('car_id')

            engine = sql.create_engine(self.connection_str)
            Session = sessionmaker(bind=engine)
            session = Session()

            session.add(new_offer)
            session.commit()

            session.close()
            return_val = new_id
        except Exception as e:
            print(f"New car addition for user {offer_args.get('user_id')} failed with error: {e}")
            return_message = f'error: {e}'
        finally:
            return return_val, return_message
    # endregion

    # region Drive
    def get_number_of_drive_reservations_by_id(self, reservation_id: str):
        return_val = None
        try:
            engine = sql.create_engine(self.connection_str)
            Session = sessionmaker(bind=engine)
            session = Session()

            query = select(Drive).where(Drive.offer_id == reservation_id)
            rez = session.execute(query)
            reservations = rez.scalars().all()

            session.close()
            return_val = len(reservations)
        except Exception as e:
            print(f'Unable to read number of reservations for id {reservation_id} for reason {e}')
        finally:
            return return_val

    def make_drive_request(self, passenger_id: str, offer_id: str):
        return_val = None
        number_of_existing_reservations = self.get_number_of_drive_reservations_by_id(offer_id)
        car_seats_for_offer = self.get_car_seats_for_offer(offer_id)
        free_seats_left = car_seats_for_offer - 1 - number_of_existing_reservations
        if free_seats_left > 0:
            return_val, return_message = self.add_new_drive(passenger_id, offer_id)
        else:
            return_message = f'Unable to make driving request for passenger {passenger_id} as no free spaces left for offer {offer_id}'

        return return_val, return_message
    # endregion

    # region Drive
    def add_new_drive(self, passenger_id: str, offer_id: str):
        return_val = None
        return_message = 'success'
        try:
            new_id = str(uuid4())
            new_drive = Drive()
            new_drive.id = new_id
            new_drive.offer_id = offer_id
            new_drive.passenger_id = passenger_id
            new_drive.reservation_date = int(datetime.timestamp(datetime.now()) * 1000)

            engine = sql.create_engine(self.connection_str)
            Session = sessionmaker(bind=engine)
            session = Session()

            session.add(new_drive)
            session.commit()

            session.close()
            return_val = new_id
        except Exception as e:
            print(f"New drive addition for passenger {passenger_id} and offer {offer_id} failed with error: {e}")
            return_message = f'error: {e}'
        finally:
            return return_val, return_message
    # endregion

    # region Complex search
    def get_offers_for_drive_request(self, request_args: Dict[str, Union[str, int]]):
        return_val = None
        drive_from = request_args.get('drive_from')
        drive_to = request_args.get('drive_to')
        drive_date = int(request_args.get('drive_date'))
        try:
            engine = sql.create_engine(self.connection_str)
            Session = sessionmaker(bind=engine)
            session = Session()

            query = "select offer_id, drive_from, drive_to, drive_date, type, seats, name, surname, role, date_of_birth, username, email from " \
                    "(select OFFERS.id as offer_id, drive_from, drive_to, drive_date, OFFERS.user_id, type, seats FROM " \
                    "OFFERS LEFT JOIN CARS on OFFERS.car_id=CARS.id) as OFFER_CAR LEFT JOIN USERS ON OFFER_CAR.user_id = USERS.id " \
                    f"where drive_from='{drive_from}' and drive_to='{drive_to}' and drive_date>{drive_date}"
            rows = session.execute(query)
            no_rows = rows.rowcount
            if no_rows > 0:
                rez_df = pd.DataFrame.from_records(rows, columns=rows.keys())
            else:
                rez_df = pd.DataFrame()
            return_val = rez_df
        except Exception as e:
            print(f"Getting offers for specified requirements failed with error {e}")
        finally:
            return return_val

    def get_car_seats_for_offer(self, offer_id: str):
        return_val = None
        try:
            engine = sql.create_engine(self.connection_str)
            Session = sessionmaker(bind=engine)
            session = Session()

            query = f"SELECT seats from OFFERS inner JOIN CARS on OFFERS.car_id=CARS.id where OFFERS.id='{offer_id}'"
            rows = session.execute(query)
            no_rows = rows.rowcount
            if no_rows == 1:
                rez_df = pd.DataFrame.from_records(rows, columns=rows.keys())
                return_val = rez_df.at[0, 'seats']
        except Exception as e:
            print(f"Getting number of car seats for offer {offer_id} failed with error {e}")
        finally:
            return return_val
    # endregion
