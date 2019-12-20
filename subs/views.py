from django.shortcuts import render
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib import messages

from .models import Sub, SubMember

class SubCreate(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Sub

class SubDetail(generic.DetailView):
    model = Sub

class SubList(generic.ListView):
    models = Sub

class SubJoin(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('subs:detail', {'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        sub = get_object_or_404(Sub, slug=self.kwargs.get('slug'))
        try:
            SubMember.objects.create(user=self.request.user, sub=sub)
        except IntegrityError:
            messages.warning(self.request, 'Warning already a member!')
        else:
            messages.success(self.request, 'You are now a member!')
        return super().get(request, *args, **kwargs)

class SubLeave(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('subs:detail', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = SubMember.objects.filter(user=self.request.user, sub__slug=self.kwargs.get('slug')).get()
        except SubMember.DoesNotExist:
            messages.warning(self.request, 'Sorry, you are not in this Sub.')
        else:
            membership.delete()
            messages.success(self.request, 'You have left the sub!')
        return super().get(request, *args, **kwargs)