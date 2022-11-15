from flask import request, current_app


def make_error(msg):
    return {'code': 400, 'msg': msg}, 400


def make_success(msg):
    return {'code': 200, 'msg': msg}, 200


def get_request_json(_request):
    try:
        request_json = request.json
    except Exception:
        current_app.logger.debug(request.data)
        # current_app.logger.debug(e)
        return None
    return request_json

