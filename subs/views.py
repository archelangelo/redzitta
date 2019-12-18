from django.shortcuts import render
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.urls import reverse
from django.views import generic

from .models import Sub, SubMember

class SubCreate(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Sub

class SubDetail(generic.DetailView):
    model = Sub

class SubList(generic.ListView):
    models = Sub
    