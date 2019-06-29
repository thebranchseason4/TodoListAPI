from django.urls import path, include
from todo import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'TodoLists', views.TodoListViewSet)

urlpatterns = [
    path('', include(router.urls))
]



