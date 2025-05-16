from django.urls import path
from base.views import users_views as views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.getUserProfileDetails, name="user-profile"),
    path('register/', views.registerUser, name='register-user'),
    path('profile/update/', views.updateUserProfileDetails, name='update-user-profile'),
    path('', views.getUsers, name="users"),
    path('delete/<int:pk>/', views.deleteUser, name="delete-user"),
    path('update/<int:pk>/', views.updateUser, name='update-user'),
    path('<int:pk>/', views.getUserById, name="user")
]