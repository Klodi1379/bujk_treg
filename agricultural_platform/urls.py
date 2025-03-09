from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import HomeView
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns (
    path('', HomeView.as_view(), name='home'),
    path('farmer/', include('farmer.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('product/', include('product.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('logistics/', include('logistics.urls')), # Ensure logistics URLs are included
    path('admin/', admin.site.urls),
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
