from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.TaskListView.as_view(),name = 'task_list'),
    path("<int:pk>/",views.TaskDetailView.as_view(), name ='task_detail'),
    path("add/",views.TaskCreateView.as_view(), name ='task_create'),
    path('<int:pk>/edit/',views.TaskUpdateView.as_view(), name ='task_update'),
    path('<int:pk>/delete/',views.TaskDeleteView.as_view(), name ='task_delete'),
    path('<int:pk>/completed/', views.CompleteTaskView.as_view(), name ='complete_task'),
    path('register/',views.SingUpView.as_view(),name = 'register'),
    path('login/',auth_views.LoginView.as_view(),name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(),name = 'logout'),
    path('archive/',views.CompletedTaskListView.as_view(),name = 'task_archive'),
    path("<int:pk>/comment/",views.CommentCreationView.as_view(),name = 'comment_create'),
    path('comment/<int:pk>/delete',views.CommentDeleteView.as_view(),name = 'comment_delete'),
    path('comment/<int:pk>/edit/',views.CommentUpdateView.as_view(),name = 'edit_comment'),
]

app_name = "tasks"