"""
URL configuration for ascentrasolutions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from .views import AdsTxtView, AppAds
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlueprintSitemap

sitemaps = {
    'blueprints': BlueprintSitemap,
}



urlpatterns = [
    path('adminvshfuewh/', admin.site.urls),
    path('', views.index, name="index"),
    path('sfs/', include("sfs.urls")),
    path('apps/', include("apps.urls")),
    path('privacy_policy/', include(("privacy_policy.urls", "privacy"), namespace="privacypolicy")),
    path('ads.txt', AdsTxtView.as_view(), name='ads_txt'),
    path('app-ads.txt', AppAds.as_view(), name='app-ads'),

    re_path(r'^\.well-known/assetlinks\.json$', serve, {
        'document_root': settings.STATICFILES_DIRS[0] / '.well-known',
        'path': 'assetlinks.json'
    }),

    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),

    path('robots.txt', views.robots_txt, name="robots"),

    path('hackathon/', include("hackathon.urls")),

]


handler404 = 'ascentracoresolutions.views.er_404'
handler400 = 'ascentracoresolutions.views.er_400'
handler401 = 'ascentracoresolutions.views.er_401'
handler403 = 'ascentracoresolutions.views.er_403'
handler408 = 'ascentracoresolutions.views.er_408'
handler500 = 'ascentracoresolutions.views.er_500'
handler502 = 'ascentracoresolutions.views.er_502'
handler503 = 'ascentracoresolutions.views.er_503'
handler504 = 'ascentracoresolutions.views.er_504'
handler505 = 'ascentracoresolutions.views.er_505'

