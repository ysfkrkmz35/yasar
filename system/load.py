from . import params

# Load Parameters

def load_prms(request):
    if not 'PRMS' in request.session:
        request.session['PRMS'] = params.PRMS
        request.session.modified = True
    return request.session['PRMS']
