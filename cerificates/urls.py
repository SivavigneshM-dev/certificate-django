from django.urls import path
from . import views

urlpatterns = [
    path('',                                    views.home,               name='home'),
    path('search/',                             views.search,             name='search'),
    path('verify/',                             views.verify,             name='verify'),
    path('verify/<uuid:certificate_id>/',       views.verify,             name='verify_with_id'),
    path('certificate/<uuid:certificate_id>/',  views.certificate_detail, name='certificate_detail'),
    path('signup/',                             views.signup_view,        name='signup'),
    path('login/',                              views.login_view,         name='login'),
    path('logout/',                             views.logout_view,        name='logout'),
    path('profile/',                            views.profile_view,       name='profile'),
]