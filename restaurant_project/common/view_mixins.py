from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class AccessRedirect(AccessMixin):
    group = "GodUser"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return redirect('login user')
        if not self.request.user.groups.filter(name__in=self.group.split(' ')).exists():
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


class BarAndKitchenAccess(AccessRedirect):
    group = "Bartenders Cooks"


class WaitersAccess(AccessRedirect):
    group = "Waiters"


