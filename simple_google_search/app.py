import os
from flask import abort, Flask, jsonify, request
from .exceptions import NotDefinedEnviromentVariable
from .logger import logger
from .custom_search import CustomSearch
from .web_search import WebSearch
from .validators import get_validator


def get_env(key):
    env = os.getenv(key)

    if not env:
        raise NotDefinedEnviromentVariable('Environment variable "{}" is required.'.format(key))

    return env


api_key = get_env('API_KEY')
cse_id = get_env('CSE_ID')

app = Flask(__name__)
custom_search = CustomSearch(api_key, cse_id)


@app.before_request
def log_request_params():
    logger.info(request.get_json())


@app.before_request
def validate():
    validator = get_validator(request.endpoint)

    validation_result = False
    if validator:
        validation_result = validator.validate(request.get_json())

    if not validation_result:
        return abort(422, {
            'status': 'NG',
            'errors': validator.errors if validator else 'Not found endpoint access.',
        })


@app.route('/search', methods=['GET'])
def search():
    req_params = request.get_json()

    search_type = req_params.get('type', 'web')
    query = req_params['query']

    if search_type == 'web':
        results = WebSearch.search(query)
    elif search_type == 'custom':
        results = custom_search.search(query)

    return jsonify({
        'results': results,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
