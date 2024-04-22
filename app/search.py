from flask import (
    Blueprint, json, jsonify, request
)
from sqlite3 import Error
from app.db import get_db

bp = Blueprint('search', __name__,)

@bp.route('/search', methods=['GET'])
def search():
    key, v = {**request.args}.popitem()
    k = "$." + key.partition('.')[2]
    db = get_db()
    try:
        with db:
            configs = db.execute("""
                SELECT name, metadata FROM configs WHERE json_extract(metadata, ?) = ?;
            """, (k, v)
            )
        j_list = []
        for config in configs:
            j_list.append(
                {"name": config[0], "metadata": json.loads(config[1])}
            )
        return jsonify(j_list)
    except Error as e:
        print(f'SELECT {key} error: {e}')
