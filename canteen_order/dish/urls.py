from django.urls import path
from .views import show_store, get_order, del_order, submit_order, del_dish, add_dish, receive_order

app_name = 'dish'
urlpatterns = [
    
    path('receive_order/', receive_order),
    path('add_dish/', add_dish),
    path('del_dish/', del_dish),
    path('submit_order/', submit_order),
    path('del_order/', del_order),
    path('get_order/', get_order),
    path('store/', show_store),
]