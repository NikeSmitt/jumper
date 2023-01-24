from django.shortcuts import render
from django.views import View


class UserSingInSingUpView(View):
    """Страница со входом или регистрацией пользователя"""
    template_name = 'account.html'
    
    def get(self, request):
        return render(request, self.template_name)
