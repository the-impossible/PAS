from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('PAS_auth.urls', namespace='auth')),
]

admin.site.site_header = "Project Allocation System"
admin.site.site_title = "Project Allocation System"
admin.site.index_title = "Welcome to Project Allocation System"