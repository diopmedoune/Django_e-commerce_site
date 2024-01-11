# shop/urls.py


from django.contrib import admin
from django.urls import path

import store.views

from ElectronicShop import settings
from django.conf.urls.static import static

import accounts.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',store.views.index, name='index'),
    path('product/<str:slug>/', store.views.product_detail, name='product-detail'),
    path('signup/', accounts.views.signup, name='signup'),
    path('logout/', accounts.views.logout_user, name='logout'),
    path('login/', accounts.views.login_user, name='login'),
    path('product/<str:slug>/add-to-cart/', store.views.add_to_cart, name='add-to-cart'),
    path('cart/', store.views.display_cart, name='display-cart'),
    path('cart/delete/', store.views.delete_cart, name='delete-cart'),
    path('cart/', store.views.display_cart, name='display-cart'),
    path('cart/delete/', store.views.delete_cart, name='delete-cart'),
    path('souhaits/', store.views.display_souhaits, name='display-souhaits'),
    path('product/<str:slug>/add-to-souhaits/', store.views.add_to_souhaits, name='add-to-souhaits'),
    path('search/', store.views.search, name='search'),
    path('ordinateurs/', store.views.get_ordinateurs, name='ordinateurs'),
    path('smartphones/', store.views.get_smartphones, name='smartphones'),
    path('cameras/', store.views.get_cameras, name='cameras'),
    path('accessoires/', store.views.get_accessoires, name='accessoires'),
    path('invoice/', store.views.display_invoice, name='display-invoice'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)