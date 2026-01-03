from django.urls import path
from manager  import views


urlpatterns=[
    path('adminhome',views.adminhome,name='adminhome'),
    path('productadd',views.productadd,name='productadd'),
    path('viewproduct',views.viewproduct,name='viewproduct'),
    path('productedit/<int:id>',views. productedit,name='productedit'),
    path('deleteproduct/<int:id>',views.deleteproduct,name='deleteproduct'),
    path('adminview',views.adminview,name='adminview'),
    path('deatilesshow/<int:id>',views.deatilesshow,name='deatilesshow'),
    path('cancel<int:id>/',views.cancel,name='cancel'),
    path('shipordr',views.shipordr,name='shipordr'),
    path('ordersts/<int:id>',views.ordersts,name='ordersts'),
    path('adminviews',views.adminviews,name='adminviews')
]