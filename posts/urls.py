from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post-list'),
    path('posts/new/', views.post_create, name = 'post-create'),
    path('posts/<int:post_id>/', views.post_detail, name= 'post-detail'),
    path('posts/<int:post_id>/edit/', views.post_update, name = 'post-update'),
    path('posts/<int:post_id>/delete/', views.post_delete, name = 'post-delete'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('mypage/<int:user_id>/', views.MyPageView.as_view(), name='mypage'),
]