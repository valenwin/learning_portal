from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module


class CourseForm(forms.ModelForm):
    image = forms.ImageField(label='Select a file 120x120', required=False)

    class Meta:
        model = Course
        fields = ('subject', 'title', 'overview', 'image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mt-2'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'overview': forms.Textarea(attrs={'class': 'form-control mt-2'}),

        }


ModuleFormSet = inlineformset_factory(Course, Module,
                                      fields=('title', 'description'),
                                      extra=3,
                                      can_delete=True)
