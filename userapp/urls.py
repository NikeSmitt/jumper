from django.urls import path
from userapp.views import UserSingInSingUpView

appname = 'userapp'

urlpatterns = [
    path('account/', UserSingInSingUpView.as_view(), name='singinup'),
]