from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo import views


router = DefaultRouter()
router.register(r'TodoLists', views.TodoListViewSet)
router.register(r'tags', views.TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
