from json import dump, load
from http import HTTPStatus
from flask import Flask, jsonify, request
from app.excepts.error_handlers import ContainsEmailError, WrongTypeError
import os

DATABASE_DIRECTORY = os.getenv('DATABASE_DIRECTORY')

app = Flask(__name__)

@app.get('/user')
def get_user():
    if os.path.exists(f'{DATABASE_DIRECTORY}/database.json'):
        with open(os.path.join(DATABASE_DIRECTORY, 'database.json'), 'r') as db_file:
            data = load(db_file)
            return jsonify({"data": data}), HTTPStatus.OK
            
    else:
        if not os.path.exists(f'{DATABASE_DIRECTORY}'):
           os.makedirs(DATABASE_DIRECTORY)
        with open(os.path.join(DATABASE_DIRECTORY, 'database.json'), 'w') as db_file:
            dump([], db_file, indent = 4)

        return jsonify({"data":[]}), HTTPStatus.OK

@app.post('/user')
def new_user():
    try:
        new_user_data = request.get_json()

        if type(new_user_data['name']) != str or type(new_user_data['email']) != str:
            raise WrongTypeError(new_user_data)

        name = new_user_data['name'].title()
        email = new_user_data['email'].lower()
        users = []

        if not os.path.exists(os.path.join(DATABASE_DIRECTORY, 'database.json')):
            os.makedirs(DATABASE_DIRECTORY)
            with open(os.path.join(DATABASE_DIRECTORY, 'database.json'), 'w') as db_file:
                dump([], db_file, indent = 4)

        with open(os.path.join(DATABASE_DIRECTORY, 'database.json'), 'r') as db_file:
            users = load(db_file)

            for user in users:
                if user['email'] == email:
                    raise ContainsEmailError("User already exists.")

            if len(users) > 0:
                last_user = users[len(users) - 1]
                new_id = last_user['id'] + 1
            else: 
                new_id = 1

            data = {
                "name": name,
                "email": email,
                "id": new_id
            }

        with open(os.path.join(DATABASE_DIRECTORY, 'database.json'), 'w') as db_file:
            users.append(data)
            dump(users, db_file, indent = 4)

            return {"data": users}, HTTPStatus.CREATED

    except ContainsEmailError as err:
        return {"error": f"{err}"}, HTTPStatus.CONFLICT
    
    except WrongTypeError as err:
        return {"wrong fields": err.wrong_fields}, HTTPStatus.BAD_REQUEST
