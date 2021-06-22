# from django.conf.urls import url

import adminapp.views as adminapp
from django.urls import re_path

app_name="adminapp"

urlpatterns = [
    re_path(r'^users/create/$', adminapp.user_create, name='user_create'),
    re_path(r'^users/read/$', adminapp.UsersListView.as_view(), name='users'),
    re_path(r'^users/update/(?P<pk>\d+)/$', adminapp.user_update, name='user_update'),
    re_path(r'^users/delete/(?P<pk>\d+)/$', adminapp.user_delete, name='user_delete'),

    re_path(r'^categories/create/$', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    re_path(r'^categories/read/$', adminapp.categories, name='categories'),
    re_path(r'^categories/update/(?P<pk>\d+)/$', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    re_path(r'^categories/delete/(?P<pk>\d+)/$', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),

    re_path(r'^products/create/category/(?P<pk>\d+)/$', adminapp.product_create, name='product_create'),
    re_path(r'^products/read/category/(?P<pk>\d+)/$', adminapp.products, name='products'),
    re_path(r'^products/read/(?P<pk>\d+)/$', adminapp.ProductDetailView.as_view(), name='product_read'),
    re_path(r'^products/update/(?P<pk>\d+)/$', adminapp.product_update, name='product_update'),
    re_path(r'^products/delete/(?P<pk>\d+)/$', adminapp.product_delete, name='product_delete'),
]