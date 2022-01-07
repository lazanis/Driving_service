import base64
import pandas as pd
from uuid import uuid4
import sqlalchemy as sql
from typing import Dict, Union

from sqlalchemy import select
from sqlalchemy.orm import declarative_base, sessionmaker

# https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html

metadata_obj = sql.MetaData()
user = sql.Table('USERS', metadata_obj,
                 sql.Column('id', sql.String, primary_key=True, default=uuid4),
                 sql.Column('name', sql.String),
                 sql.Column('surname', sql.String),
                 sql.Column('role', sql.String),
                 sql.Column('date_of_birth', sql.BIGINT),
                 sql.Column('username', sql.String),
                 sql.Column('pwd', sql.String),
                 sql.Column('email', sql.String))

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
            connection = engine.connect()
        except Exception as e:
            print(f'Checking if user exists by username failed with error: {e}')
        else:
            # filter column
            column = sql.column('username')
            # get columns
            query = user.select().with_only_columns(user.columns.id)
            query = query.where(column == username)
            rows = connection.execute(query)
            no_rows = rows.rowcount
            if no_rows == 1:
                rez_df = pd.DataFrame.from_records(rows, columns=rows.keys())
                return_val = rez_df.at[0, 'id']
            connection.close()
        finally:
            return return_val

    def write_new_user(self, user_dict: Dict[str, Union[int, str, bytes]]):
        return_val = None
        return_message = 'success'
        try:
            engine = sql.create_engine(self.connection_str)
            connection = engine.connect()
            query = user.insert()
            new_id = str(uuid4())
            user_pwd = user_dict.get('pwd')
            user_pwd = user_pwd.encode('utf-8')
            user_pwd = base64.b64encode(user_pwd)

            user_dict['id'] = new_id
            user_dict['pwd'] = user_pwd
            user_dict['date_of_birth'] = int(user_dict['date_of_birth'])

            query = query.values(user_dict)

            connection.execute(query)
            connection.close()
            return_val = new_id
        except Exception as e:
            print(f'Checking if user exists by username failed with error: {e}')
            return_message = f'error: {e}'
        finally:
            return return_val, return_message

    def get_all_users(self):
        engine = sql.create_engine(self.connection_str)
        connection = engine.connect()

        Session = sessionmaker(bind=engine)
        session = Session()

        query = select(User)
        rez = session.execute(query)
        users = rez.scalars().all()
        for u in users:
            print(u)
        x = 5
        session.close()
    # endregion
