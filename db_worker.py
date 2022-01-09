import base64
from uuid import uuid4
import sqlalchemy as sql
from typing import Dict, Union
from sqlalchemy import select, and_
from sqlalchemy.orm import sessionmaker
from data_classes import User, Car, Offer


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
