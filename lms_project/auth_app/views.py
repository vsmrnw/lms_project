from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import LoginForm, RegisterForm
from datetime import datetime


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    next_page = 'index'

    def form_valid(self, form):
        is_remember = self.request.POST.get('is_remember')
        if is_remember == 'on':
            self.request.session[settings.REMEMBER] = datetime.now().isoformat()
            self.request.session.set_expire(settings.REMEMBER_AGE)
        elif is_remember == 'off':
            self.request.session.set_expire(0)
        return super(UserLoginView, self).form_valid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save()
        pupil = Group.objects.filter(name='Ученик')
        user.groups.set(pupil)
        login(self.request, user)
        return redirect('index')
