# reflections/views.py

from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Reflection
from .forms import ReflectionForm


class ReflectionListView(ListView):
    model = Reflection
    template_name = 'reflections/reflection_list.html'
    context_object_name = 'reflections'


class ReflectionDetailView(DetailView):
    model = Reflection
    template_name = 'reflections/reflection_detail.html'
    context_object_name = 'reflection'


class ReflectionCreateView(LoginRequiredMixin, CreateView):
    model = Reflection
    form_class = ReflectionForm
    template_name = 'reflections/reflection_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class ReflectionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reflection
    form_class = ReflectionForm
    template_name = 'reflections/reflection_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('reflection-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        reflection = self.get_object()
        return self.request.user.profile == reflection.owner or self.request.user.profile.user_type == 'admin_teacher'


class ReflectionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reflection
    template_name = 'reflections/reflection_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('reflection-list')

    def test_func(self):
        reflection = self.get_object()
        return self.request.user.profile == reflection.owner or self.request.user.profile.user_type == 'admin_teacher'
