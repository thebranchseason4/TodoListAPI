from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo import views


from todo import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'TodoLists', views.TodoListViewSet)
router.register(r'tags', views.TagViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
