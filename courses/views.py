from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import CourseForm
from .models import Course


class ManageCourseListView(ListView):
    model = Course
    template_name = 'list.html'

    def get_queryset(self):
        qs = super(ManageCourseListView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerUpdateMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerUpdateMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('courses:manage_course_list')


class OwnerCourseUpdateMixin(OwnerCourseMixin, OwnerUpdateMixin):
    form_class = CourseForm
    success_url = reverse_lazy('courses:manage_course_list')
    template_name = 'form.html'


class CourseCreateView(PermissionRequiredMixin,
                       OwnerCourseUpdateMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseUpdateMixin, UpdateView):
    form = CourseForm()
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin, DeleteView):
    template_name = 'delete.html'
    success_url = reverse_lazy('courses:manage_course_list')
    permission_required = 'courses.delete_course'
