from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from ..forms import CommentForm
from ..models import Comment
from .login import check_dev, check_project, check_client


# Vistas modelo Comment
@login_required
def comment_list_filter(request, pk):
    comment = Comment.objects.filter(task=pk)
    context = {'comment': comment}
    return render(request, 'project_task/comment_list_filter.html', context)


class CommentCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "project_task/comment_create.html"

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        clie = check_client(self.request.user)
        return prod or dev or clie

    success_url = reverse_lazy('projectman:list_comment')


class CommentList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Comment
    template_name = 'project_task/comment_list.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        clie = check_client(self.request.user)
        return prod or dev or clie


class CommentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'project_task/comment_create.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        clie = check_client(self.request.user)
        return prod or dev or clie

    success_url = reverse_lazy('projectman:list_comment')


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'inclusion_tags/modal_eliminar.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        return prod or dev

    success_url = reverse_lazy('projectman:list_comment')


class CommentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Comment
    template_name = 'project_task/comment_detail.html'

    def test_func(self):
        dev = check_dev(self.request.user)
        prod = check_project(self.request.user)
        clie = check_client(self.request.user)
        return prod or dev or clie


@login_required
def modalComment(request):
    return render(request, 'project_task/prueba_modal.html', {})
