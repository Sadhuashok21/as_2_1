from django.urls import path, include
from . import views

urlpatterns = [


    # sign in
    path('sign_in/create_account', views.create_account, name="create_account"),
    path('sign_in/signin', views.signin, name="sign_in"),

    # insertions 
    path('insertions/activity_insert', views.all_insert, name="all_insert"),
    path('insertions/error_insert', views.error_insert, name="error_insert"),
    path('insertions/insert_id', views.insert_id, name="insert_id"),
    path('ip/', views.ip_info_view, name="ip_info"),

    #sign in
    path('sign_in/create_account', views.create_account, name="sign_create"),
    path('sign_in/updateid', views.updateid, name="sign_update"),


    #sfs blueprints version 2.0.87

    path('sfs_blueprints/2_0_87/in_blueprint', views.blueprint_2_0_87, name="blueprint_2_0_87"),
    path('sfs_blueprints/2_0_87/rand_blueprint', views.rand_blueprints_2_0_87, name="rand_blueprint_2_0_87"),

    # sfs blueprints version 2.0.89
    path('sfs_blueprints/2_0_89/home_blueprints', views.home_blueprints, name="home_blueprints"),
    path('sfs_blueprints/2_0_89/home_plawor', views.home_plawor, name="home_plawor"),
    path('sfs_blueprints/2_0_89/category', views.home_category, name="home_category"),
    path('sfs_blueprints/2_0_89/blueprints', views.blueprints, name="blueprints1"),
    path('sfs_blueprints/2_0_89/blueprints_off', views.blueprints_off, name="blueprints_off"),
    path('sfs_blueprints/2_0_89/category_off', views.home_category_off, name="category_off"),
    path('sfs_blueprints/2_0_89/page', views.page, name="page"),
    path('sfs_blueprints/2_0_89/pla_page', views.pla_page, name="pla_page"),
    path('sfs_blueprints/2_0_89/signin', views.home_category, name="signin2"),


    #sfs blueprints 2_0_9
    path('sfs_blueprints/2_0_9/blueprints', views.blueprints_2_0_9, name="blueprints_2_0_9"),
    path('sfs_blueprints/2_0_9/pla_wor', views.pla_2_0_9, name="pla_2_0_9"),
    path('sfs_blueprints/2_0_9/category', views.category_2_0_9, name="category_2_0_9"),
    path('sfs_blueprints/2_0_9/blueprint', views.blueprint_2_0_9, name="blueprint_2_0_9"),
    path('sfs_blueprints/2_0_9/inner_bp', views.inner_bp, name="more_blueprints"),
    path('sfs_blueprints/2_0_9/', views.all_insert, name="all_insert"),
    path('sfs_blueprints/2_0_9/bp_pla_id', views.insert_id, name="insert_id"),

    
    #path('sfs_blueprints/2_0_9/blueprints', views),

    # Fresh Basket Goo
    # path('fresh_basket/0_1/products', views.products, name="products"),
    # path('fresh_basket/0_1/orders', views.orders, name="orders"),
    # path('fresh_basket/0_1/fb_sign_in', views.fb_sign_in, name="fb_sign_in"),
    # path('fresh_basket/0_1/fb_create_account', views.fb_create_account, name="fb_create_account"),

]