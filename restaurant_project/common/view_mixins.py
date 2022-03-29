from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class AccessRedirect(AccessMixin):
    group = "GodUser"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return redirect('login user')
        if not self.request.user.groups.filter(name=self.group).exists():
            # Redirect the user to somewhere else - add your URL here
            return redirect('index')

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)


class BartendersAccess(AccessRedirect):
    group = "Bartenders"

class CooksAccess(AccessRedirect):
    group = "Cooks"

class WaitersAccess(AccessRedirect):
    group = "Waiters"
