from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('PAS_auth.urls', namespace='auth')),
    path('assess/', include('PAS_assessment.urls', namespace='assess')),
    path('hall/', include('PAS_hallAllocation.urls', namespace='hall')),
    path('payment/', include('PAS_payment.urls', namespace='payment')),
    path('', include('PAS_app.urls', namespace='app')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Project Allocation System"
admin.site.site_title = "Project Allocation System"
admin.site.index_title = "Welcome to Project Allocation System"