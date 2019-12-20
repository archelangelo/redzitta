from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()

from . import models

class PostList(ListView):
    model = models.Post

class UserPosts(ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(DetailView):
    model = models.Post

class PostDelete(DeleteView):
    model = models.Post

class PostCreate(LoginRequiredMixin, CreateView):
    fields = ['message', 'sub']
    model = models.Post

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostDelete(LoginRequiredMixin, DeleteView):
    model = models.Post
    success_url = reverse_lazy('posts:list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)