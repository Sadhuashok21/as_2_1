from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.blueprints, name="blueprintss"),
    path('home', views.home, name="home"),
    path('blueprints', views.blueprints, name="blueprints"),
    path('blueprints/', views.blueprints, name="blueprints_slash"),
    path('bp/download/<str:bp_id>', views.download, name="download"),
    path('blueprints/blueprint', views.blueprint, name="blueprint"),
    path('planetsandworlds', views.planetsandworlds, name="planetsandworlds"),
    path('planetsandworlds/', views.planetsandworlds, name="planetsandworlds_slash"),
    path('profile', views.profile, name="profile"),
    path('profile/favorites', views.favorites, name="favorites"),
    path('profile/favorites/add_favorite', views.add_favourite, name="add_favorite"),
    path('access_denied', views.access_denied, name="access_denied"),
    path('uploads', views.Upload.as_view(), name="uploads"),
    path('upload_category', views.UploadCat.as_view(), name="upload_category"),
    path('search', views.search, name="search"),
    path('planetsandworlds/search', views.search, name="pla_search"),
    path('blueprints/category', views.category, name="category"),
    path('logout', views.logout, name="logout"),

    
]
