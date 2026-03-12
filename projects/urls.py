from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('create-project/', views.create_project, name='create_project'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/join/', views.join_project, name='join_project'),
    path('<int:project_id>/complete/', views.complete_project, name='complete_project'),
    path('api/<int:project_id>/favorite/', views.add_favorite, name='add_favorite'),
    path('api/<int:project_id>/unfavorite/', views.remove_favorite, name='remove_favorite'),
]