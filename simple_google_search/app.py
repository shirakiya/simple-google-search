from flask import abort, Flask, jsonify, request
from .logger import logger
from .google_search import GoogleSearch
from .validators import get_validator

app = Flask(__name__)


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
            'errors': validator.errors,
        })


@app.route('/search', methods=['GET'])
def search():
    req_params = request.get_json()

    result = GoogleSearch.search(req_params['query'])

    return jsonify({
        'result': result,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
