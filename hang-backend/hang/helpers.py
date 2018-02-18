import os
from functools import wraps
from . import configs 
from flask import request, abort

'''
Returns current app environment
'''
def get_current_env():
    return os.getenv('APP_ENV') or 'dev'

'''
Check if a given request has keys 
'''
def request_has_key(rqst):
    return rqst.args.get('key') and rqst.args.get('key') == configs[get_current_env()].SECRET_KEY

'''
Wrapper for methods that require an API key
'''
def require_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request_has_key(request):
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper