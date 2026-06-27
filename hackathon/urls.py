from django.urls import path

from .views import *


urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home', home, name='hack_home'),

    path('home/team', teams, name="teams"),


    path('home/submission', SubmissionView.as_view(), name='submission'),
    path('home/challenges', challenges, name="challenges"),
    path('login/', LogIn.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),

    path('payment/', payment, name='payment'),
    path("save-payment/", save_payment, name="save-payment"),
    path('evaluation/', EvaluationView.as_view(), name='evaluation'),
    path('judge-assign/', AssignJudgeView.as_view(),  name="assign_judge"),
    path('scoreboard/', ScoreBoardView.as_view(), name='scoreboard'),

]
