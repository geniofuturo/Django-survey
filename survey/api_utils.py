from django.utils import simplejson as json
from extjs import utils

def response(request, qs, grid_klass):
    """
    generate a standard extjs response
    """
    grid = grid_klass()
    qs = grid.query_from_request(request, qs)
    resp = grid.get_rows_json(qs)
    return utils.JsonResponse(resp)

def success():
    resp = json.JSONEncoder(ensure_ascii=False).encode({
        'success':True, 
    })
    return utils.JsonResponse(resp)

def response_error(request, form):
    """
    generate an error response
    """
    json_data = request.REQUEST.get('data', [])
    decoded_data = json.loads(json_data)
    resp = json.JSONEncoder(ensure_ascii=False).encode({
        'success':False,
        'message': unicode(form.errors),
        'data': decoded_data
    })
    return utils.JsonResponse(resp)
    

def load_form(request, form_klass): 
    """
    load form from submited extjs data
    """
    json_data = request.REQUEST.get('data', [])
    decoded_data = json.loads(json_data)
    form = form_klass(decoded_data)
    return form

def coerce_put_post(request):
    """
    Django doesn't particularly understand REST.
    In case we send data over PUT, Django won't
    actually look at the data and load it. We need
    to twist its arm here.
    
    The try/except abominiation here is due to a bug
    in mod_python. This should fix it.
    """
    if request.method == "PUT":
        # Bug fix: if _load_post_and_files has already been called, for
        # example by middleware accessing request.POST, the below code to
        # pretend the request is a POST instead of a PUT will be too late
        # to make a difference. Also calling _load_post_and_files will result 
        # in the following exception:
        #   AttributeError: You cannot set the upload handlers after the upload has been processed.
        # The fix is to check for the presence of the _post field which is set 
        # the first time _load_post_and_files is called (both by wsgi.py and 
        # modpython.py). If it's set, the request has to be 'reset' to redo
        # the query value parsing in POST mode.
        if hasattr(request, '_post'):
            del request._post
            del request._files
        
        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'
            
        request.PUT = request.POST
