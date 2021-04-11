from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
import django_pydenticon.urls
from django_pydenticon.views import image as pydenticon_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('identicon/image/<path:data>/', pydenticon_image, name='pydenticon_image'),

    path('accounts/', include('accounts.urls')),
    path('', include('instagram.urls')),
    path('', login_required(TemplateView.as_view(template_name='root.html')), name='root'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                        document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]               

