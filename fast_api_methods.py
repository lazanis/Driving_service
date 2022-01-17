from db_worker import DBWorker
from fastapi import FastAPI, Request

app = FastAPI()
db_worker = DBWorker(address="192.168.1.5")


@app.post("/register")
def register(request: Request):
    ret_dict = {'unique_id': None, 'message': None}

    request_args = dict(request.query_params)
    ret_val = db_worker.check_if_user_exists_by_username(request_args.get('username'))

    if ret_val is not None:
        ret_dict['unique_id'] = -1
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
    ret_val, ret_role = db_worker.check_if_user_exists_by_username_and_pwd(request_args.get('username'), request_args.get('pwd'))
    if ret_val is not None:
        ret_dict['unique_id'] = ret_val
        ret_dict['message'] = f'Successful login for user {ret_val} with role {ret_role}'
    else:
        ret_dict['unique_id'] = -1
        ret_dict['message'] = f'Unable to login as username and/or password are wrong'

    return ret_dict


@app.post('/add_new_car')
def add_new_car(request: Request):
    ret_dict = {'unique_id': None, 'message': None}

    request_args = dict(request.query_params)
    ret_val, return_message = db_worker.write_new_car(request_args)
    if ret_val is not None:
        ret_dict['unique_id'] = ret_val
        ret_dict['message'] = f"Successful car addition with id {ret_val} for user {request_args.get('user_id')}"
    else:
        ret_dict['unique_id'] = -1
        ret_dict['message'] = f'Unable to add new car for user'

    return ret_dict


@app.get('/get_all_cars_for_user')
def get_all_cars_for_user(request: Request):
    ret_dict = {'cars_number': None, 'cars': None}

    request_args = dict(request.query_params)
    ret_val = db_worker.get_all_cars_for_user(request_args.get('user_id'))
    if ret_val is not None:
        ret_dict['cars_number'] = len(ret_val)
    else:
        ret_dict['cars_number'] = -1
    ret_dict['cars'] = ret_val

    return ret_dict


@app.post('/add_new_offer')
def add_new_offer(request: Request):
    ret_dict = {'unique_id': None, 'message': None}

    request_args = dict(request.query_params)
    ret_val, return_message = db_worker.add_new_offer(request_args)
    if ret_val is not None:
        ret_dict['unique_id'] = ret_val
        ret_dict['message'] = f"Successful offer addition with id {ret_val} for user {request_args.get('user_id')}"
    else:
        ret_dict['unique_id'] = -1
        ret_dict['message'] = f'Unable to add new offer for user'

    return ret_dict


@app.get('/get_driving_offers')
def make_driving_reservation(request: Request):
    ret_dict = {'offers_number': None, 'offers': None}

    request_args = dict(request.query_params)
    ret_val = db_worker.get_offers_for_drive_request(request_args)
    if ret_val is not None:
        ret_dict['offers_number'] = len(ret_val)
        ret_dict['offers'] = ret_val.to_dict(orient='index')
    else:
        ret_dict['offers_number'] = -1
        ret_dict['offers'] = dict()

    return ret_dict


@app.post('/make_driving_reservation')
def make_driving_reservation(request: Request):
    ret_dict = {'unique_id': None, 'message': None}

    request_args = dict(request.query_params)
    ret_val, return_message = db_worker.make_drive_request(request_args.get('passenger_id'), request_args.get('offer_id'))
    if ret_val is not None:
        ret_dict['unique_id'] = ret_val
        ret_dict['message'] = f"Successful drive request made for offer {request_args.get('offer_id')}"
    else:
        ret_dict['unique_id'] = -1
        ret_dict['message'] = f'Unable to add new drive request'

    return ret_dict


@app.get('/get_past_drives')
def get_past_drives(request: Request):
    ret_dict = {'past_drives_number': None, 'past_drives': None}

    request_args = dict(request.query_params)
    user_id = request_args.get('user_id')
    ret_val = db_worker.get_past_drives_for_user(user_id)
    if ret_val is not None:
        ret_dict['past_drives_number'] = len(ret_val)
    else:
        ret_dict['past_drives_number'] = -1
    ret_dict['past_drives'] = ret_val.to_dict(orient='index')

    return ret_dict


@app.post('/add_review')
def add_review(request: Request):
    ret_dict = {'unique_id': None, 'message': None}

    request_args = dict(request.query_params)
    ret_val, return_message = db_worker.add_new_review(request_args)
    if ret_val is not None:
        ret_dict['unique_id'] = ret_val
        ret_dict['message'] = f"Successful review addition with id {ret_val} from user {request_args.get('user_id')}"
    else:
        ret_dict['unique_id'] = -1
        ret_dict['message'] = f'Unable to add new offer for user'

    return ret_dict
