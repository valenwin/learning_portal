from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from courses.fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    image = models.ImageField(upload_to='courses_images/%Y/%m/%d',
                              blank=True,
                              null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.title
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    # def get_absolute_url(self):
    #     return reverse('courses:course_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('courses:course_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('courses:course_delete', kwargs={'slug': self.slug})


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = OrderField(blank=True, for_fields=['course'])
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f'{self.order}: {self.title}'


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={
                                         'model__in': ('text', 'video', 'image', 'file')
                                     })
    object_id = models.PositiveIntegerField()
    order = OrderField(blank=True, for_fields=['module'])
    item = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('order',)


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',  # text_related,file_related,image_related,video_related
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
