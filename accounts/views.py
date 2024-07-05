from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView
from .models import Profile, ClassName
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import ExtendedUserCreationForm, ClassForm


class HomePageView(TemplateView):
    template_name = 'accounts/home.html'


class ProfileCreateView(LoginRequiredMixin, CreateView):
    form_class = ExtendedUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('profile-list')

    def dispatch(self, *args, **kwargs):
        if not self.request.user.profile.user_type == 'admin_teacher':
            return self.handle_no_permission()  # Redirect non-admin teachers
        return super().dispatch(*args, **kwargs)


class ProfileListView(ListView):
    model = Profile
    template_name = 'accounts/profiles_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        queryset = Profile.objects.all()
        user_type = self.request.GET.get('user_type', None)
        search_query = self.request.GET.get('search', None)

        if user_type:
            queryset = queryset.filter(user_type=user_type)

        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(class_name__name__icontains=search_query) |
                Q(user_type__icontains=search_query)
            )

        return queryset


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'


class ClassListView(ListView):
    model = ClassName
    template_name = 'accounts/class_list.html'
    context_object_name = 'classes'

    def get_queryset(self):
        queryset = ClassName.objects.all()
        search_query = self.request.GET.get('search', None)
        book_filter = self.request.GET.get('book', None)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(teacher__icontains=search_query)
            )

        if book_filter:
            queryset = queryset.filter(book=book_filter)

        return queryset


class ClassDetailView(DetailView):
    model = ClassName
    template_name = 'accounts/class_detail.html'
    context_object_name = 'class'


class ClassCreateView(LoginRequiredMixin, CreateView):
    model = ClassName
    form_class = ClassForm
    template_name = 'accounts/class_form.html'
    success_url = reverse_lazy('class-list')

    def test_func(self):
        return self.request.user.profile.user_type == 'admin_teacher'
