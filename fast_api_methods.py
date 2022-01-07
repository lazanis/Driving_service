from db_worker import DBWorker
from fastapi import FastAPI, Request

app = FastAPI()
db_worker = DBWorker()


@app.post("/register")
def register(request: Request):
    ret_dict = {'unique_id': None, 'message': None}

    request_args = dict(request.query_params)
    ret_val = db_worker.check_if_user_exists_by_username(request_args.get('username'))

    if ret_val is not None:
        ret_dict['unique_id'] = ret_val
        ret_dict['message'] = 'User with desired username already existing'
    else:
        ret_val, return_message = db_worker.write_new_user(request_args)
        if ret_val is not None:
            ret_dict['unique_id'] = ret_val
            ret_dict['message'] = f'New user registered with id {ret_val}'
        else:
            ret_dict['unique_id'] = -1
            ret_dict['message'] = f'Unable to register new user registered for error: {return_message}'

    return ret_dict


@app.get('/login')
def login(request: Request):
    ret_dict = {'unique_id': None, 'message': None}

    request_args = dict(request.query_params)
    ret_val = db_worker.check_if_user_exists_by_username_and_pwd(request_args.get('username'), request_args.get('pwd'))
    if ret_val is not None:
        ret_dict['unique_id'] = ret_val
        ret_dict['message'] = f'Successful login for user {ret_val}'
    else:
        ret_dict['unique_id'] = -1
        ret_dict['message'] = f'Unable to login as username and/or password are wrong'

    return ret_dict
