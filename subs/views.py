from django.shortcuts import render
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.urls import reverse
from django.views import generic

from .models import Sub, SubMember

class CreateSubView(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Sub

class SubDetailView(generic.DetailView):
    model = Sub

class SubListView(generic.ListView):
    models = Sub
    