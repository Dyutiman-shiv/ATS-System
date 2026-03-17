from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^summernote/', include('django_summernote.urls')),

    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),

    # Anything else should go to core app
    re_path('^', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.about.error_404'
handler500 = 'core.views.about.error_500'

admin.site.site_header = 'HireSure Admin'
admin.site.site_title = 'HireSure Admin Interface'

