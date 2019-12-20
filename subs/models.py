from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import template

import misaka

User = get_user_model()
register = template.Library()

class Sub(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(blank=True, editable=False, default='')
    members = models.ManyToManyField(User, through='SubMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('subs:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']


class SubMember(models.Model):
    sub = models.ForeignKey(Sub, related_name='sub_members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_subs', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub', 'user'], name='unique_membership'),
        ]


