from django.urls import path 
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLogin, CustomRegister
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # by default, the ListView looks for a template with the name of model _list.html 
    path('', TaskList.as_view(), name="tasks"),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task/new/', TaskCreate.as_view(), name='task-create'),
    path('task/edit/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task/delete/<int:pk>', TaskDelete.as_view(), name='task-delete'),
    path('login/', CustomLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', CustomRegister.as_view(), name='register'),
]
