from flask import (
    abort, Blueprint, json, jsonify, request
)
from sqlite3 import IntegrityError, DataError
from app.db import get_db

bp = Blueprint('configs', __name__, url_prefix='/configs')

def get_handled_configs(configs):
    j_list = [{"name": config[0], "metadata": json.loads(config[1])}
                for config in configs
            ]
    return j_list


def get_payload_args(payload):
    payload = request.get_json()
    name = payload["name"]
    metadata = json.dumps(payload["metadata"])
    return name, metadata


@bp.route('/', methods=['GET'])
def list():
    db = get_db()
    try:
        with db:
            configs = db.execute("""
                                SELECT name, metadata
                                FROM configs
                                ORDER BY name
                                ;"""
            )

        j_list = get_handled_configs(configs)

        if len(j_list) == 0:
            abort(404, f'There are no configs!')

        return jsonify(j_list)
    except DataError as e:
        print(f'SELECT all configs error: {e}')


@bp.route('/', methods=['POST'])
def create():
    if request.is_json:
        name, metadata = get_payload_args(request.get_json())
        db = get_db()
        try:
            with db:
                db.execute("""
                            INSERT INTO configs (name, metadata)
                            VALUES (?, ?)
                            ;"""
                            ,(name, metadata)
                )
            return f"INSERT {name} was successful\n"
        except IntegrityError as e:
            print(f'INSERT {name} error: {e}')
    else:
        return "payload is not in json"


@bp.route('/<name>', methods=['GET'])
def get(name):
    db = get_db()
    try:
        with db:
            configs = db.execute("""
                                SELECT name, metadata
                                FROM configs
                                WHERE name = ?
                                ;"""
                                , (name,)
            )
        j_list = get_handled_configs(configs)

        if len(j_list) == 0:
            abort(404, f'There is no {name} config!')

        return jsonify(j_list)
    except DataError as e:
        print(f'SELECT {name} error: {e}')


@bp.route('/<name>', methods=['PUT'])
def update_put(name):
    if request.is_json:
        name, metadata = get_payload_args(request.get_json())
        db = get_db()
        try:
            with db:
                db.execute("""
                            REPLACE INTO configs (name, metadata)
                            VALUES (?, ?)
                            ;"""
                            ,(name, metadata)
                )
            return "REPLACE {name} was successful\n"

        except IntegrityError as e:
            print(f'REPLACE {name} error: {e}')
    else:
        return "payload is not in json"


@bp.route('/<name>', methods=['PATCH'])
def update_patch(name):
    if request.is_json:
        name, metadata = get_payload_args(request.get_json())
        db = get_db()
        try:
            with db:
                db.execute("""
                            UPDATE configs
                            SET metadata = ?
                            WHERE name = ?
                            ;"""
                            ,(metadata, name)
                )
            return "UPDATE {name} was successful\n"

        except IntegrityError as e:
            print(f'UPDATE {name} error: {e}')
    else:
        return "payload is not in json"


@bp.route('/<name>', methods=['DELETE'])
def delete(name):
    db = get_db()
    try:
        with db:
            db.execute("""
                        DELETE FROM configs
                        WHERE name = ?
                        ;"""
                        , (name,)
            )
        return f'DELETE {name} was successful\n'

    except IntegrityError as e:
        print(f'DELETE {name} error: {e}')
