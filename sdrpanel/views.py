from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class CustomLogoutView(BaseLogoutView):
    http_method_names = ["get", "post", "options"]
    template_name = "registration/logged_out.html"
    extra_context = None

    @method_decorator(csrf_exempt)
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)
