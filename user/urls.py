from django.urls import path
from user import views
from user.views import (
    
    CancelView,
    SuccessView,
    
)


urlpatterns=[
    path('',views.home,name='home'),
    path('registration',views.registration,name='registration'),
    path('userhome',views.userhome,name='userhome'),
    path('login_user',views.login_user,name='login_user'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('deatiles/<int:id>',views.deatiles,name='deatiles'),
    path('addcart',views.addcart,name='addcart'),
    path('viewcart',views.viewcart,name='viewcart'),
    path('trash/<int:id>',views.trash,name='trash'),
    path('addproduct/<int:id>',views.addproduct,name='addproduct'),
    path('deletecart/<int:id>',views.deletecart,name='deletecart'),
    path('summary',views.summary,name='summary'),
    path('viewprofile',views.viewprofile,name='viewprofile'),
    path('edit_profile/<int:id>',views.edit_profile,name='edit_profile'),
    path('addwhis/<int:id>',views.addwhis,name='addwhis'),
    path('toggle_wishlist/<int:id>',views.toggle_wishlist,name='toggle_wishlist'),
    path('viewwish',views.viewwish,name='viewwish'),
    path('checkout',views.checkout,name="checkout"),
    path('cancel/',CancelView.as_view(),name="canel"),
    path('success/', SuccessView.as_view(), name='success'),
    path('search',views.search,name='search')

]