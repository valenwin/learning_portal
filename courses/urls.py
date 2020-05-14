from django.urls import path

from .views import ManageCourseListView
from .views import CourseCreateView, CourseUpdateView, CourseDeleteView

urlpatterns = [
    path('my-list/', ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<str:slug>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<str:slug>/delete/', CourseDeleteView.as_view(), name='course_delete'),

]
