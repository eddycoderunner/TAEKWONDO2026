from django.urls import path
from . import views
from . import views_draws
from . import views_bracket

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('update/', views.update_view, name='update'),
    path('athletes/', views.athletes_list, name='athletes'),
    path('draws/', views_draws.draws_view, name='draws'),                      
    path('bracket/', views_bracket.bracket_view, name='bracket'),              
    path('bracket/data/', views_bracket.get_bracket_data, name='bracket_data'), 
    path('bracket/save/', views_bracket.save_bracket, name='save_bracket'),    
]