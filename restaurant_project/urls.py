from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/', include('restaurant_project.accounts.urls')),
                  path('', include('restaurant_project.main.urls')),
                  path('waiters/', include('restaurant_project.waiters.urls')),
                  path('kitchen/', include('restaurant_project.kitchen.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
