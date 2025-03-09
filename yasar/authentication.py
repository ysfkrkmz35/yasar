from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect

class LoginView(auth_views.LoginView):

    def dispatch(self, request, *args, **kwargs):

        if self.request.path == '/login/' or self.request.path == '/logout/':
            request.next = '/'

        return super().dispatch(request, *args, **kwargs)

def logout_view(request):
    redirect = request.GET.get('redirect')

    if redirect is not None:
        redirect = request.GET.get('redirect')
    else:
        redirect = '/login'

    logout(request)
    return HttpResponseRedirect(redirect)
