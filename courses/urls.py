from django.urls import path

from .views import CourseCreateView, CourseUpdateView, CourseDeleteView
from .views import CourseModuleUpdateView
from .views import ManageCourseListView
from .views import ModuleContentListView
from .views import ContentCreateUpdateView, ContentDeleteView

urlpatterns = [
    path('my-list/', ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<str:slug>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<str:slug>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    path('<int:pk>/module/', CourseModuleUpdateView.as_view(), name='course_module_update'),
    path('module/<int:module_id>', ModuleContentListView.as_view(), name='module_content_list'),

    path('module/<int:module_id>/content/<model_name>/create/', ContentCreateUpdateView.as_view(),
         name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<int:id>/', ContentCreateUpdateView.as_view(),
         name='module_content_update'),
    path('content/<int:id>/delete/', ContentDeleteView.as_view(), name='module_content_delete'),
]
