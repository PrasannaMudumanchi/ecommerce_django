from django.urls import path
from . import views
app_name ="ecommerce_site"
urlpatterns = [
    path("", views.Index.as_view(), name='index'),
    path("product/<slug>/", views.ItemDetailedView.as_view(), name='product'),
    path("add_to_cart/<slug>/", views.add_to_cart, name='add_to_cart'),
    path("remove_cart/<slug>/", views.remove_from_cart, name='remove_cart'),
    path('remove_single_item_from_cart/<slug>/', views.remove_single_item_from_cart,
         name='remove_single_item_from_cart'),
    path('checkout/',views.checkout1,name ="checkout"),
    path("order-summery/", views.OrderSummery.as_view(), name='order_summery'),

]
