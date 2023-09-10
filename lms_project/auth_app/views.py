from datetime import datetime

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from .forms import LoginForm, RegisterForm
from .signals import account_access


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    next_page = 'index'

    def form_valid(self, form):
        is_remember = self.request.POST.get('is_remember')
        if is_remember == 'on':
            self.request.session[settings.REMEMBER_KEY] = \
                datetime.now().isoformat()
            self.request.session.set_expiry(settings.REMEMBER_AGE)
        elif is_remember == 'off':
            self.request.session.set_expiry(0)

        account_access.send(sender=self.__class__, request=self.request)

        return super(UserLoginView, self).form_valid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = 'index'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)
