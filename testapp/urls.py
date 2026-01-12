from django.urls import path,include
from . import views
from django.urls import path
from .views import PostListAPIView
urlpatterns = [
    path('', views.timeline, name='timeline'), 
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post_create', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('api/posts/', PostListAPIView.as_view(), name='post_list_api'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('api/weather/', views.weather, name='weather'),
    path('pokemon/', views.pokemon_viewer, name='pokemon_viewer'),
]