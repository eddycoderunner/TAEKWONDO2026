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
    path('admin/draws/', views_draws.draws_view, name='draws'),
    path('admin/bracket/', views_bracket.bracket_view, name='bracket'),
    path('admin/bracket/data', views_bracket.get_bracket_data, name='bracket_data'),
    path('admin/bracket/save', views_bracket.save_bracket, name='save_bracket'),
]