from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View

from .forms import CourseForm, ModuleFormSet
from .models import Course, Module, Content


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


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
                             data=data)

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, id=kwargs.get('pk'),
                                        owner=request.user)
        return super().dispatch(request, kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:manage_course_list')
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
    For create and update different types of content:
    'text', 'video', 'image', 'file'.
    """
    module = None
    model = None
    obj = None
    template_name = 'content/form.html'

    def get_model(self, model_name):
        if model_name in ('text', 'video', 'image', 'file'):
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner', 'order',
                                                 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({
            'form': form,
            'object': self.obj
        })

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('courses:module_content_list', self.module.id)

        return self.render_to_response({
            'form': form,
            'object': self.obj
        })


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module_content_list', module.id)
