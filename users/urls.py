
# from django.urls import path
# from django.contrib.auth import views as auth_views
# from django.conf import settings
# from django.conf.urls.static import static
# from . import views
# from .forms import CustomAuthForm

# urlpatterns = [
#     path('register/', views.register, name='register'),
#     path('login/', views.login, name='login',kwargs={"authentication_form":CustomAuthForm}),
#     path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
#     path('info/', views.info, name='info'),
#     path('password-reset/',
#          auth_views.PasswordResetView.as_view(
#              template_name='password_reset.html'
#          ),
#          name='password_reset'),
#     path('password-reset/done/',
#          auth_views.PasswordResetDoneView.as_view(
#              template_name='password_reset_done.html'
#          ),
#          name='password_reset_done'),
#     path('password-reset-confirm/<uidb64>/<token>/',
#          auth_views.PasswordResetConfirmView.as_view(
#              template_name='password_reset_confirm.html'
#          ),
#          name='password_reset_confirm'),
#     path('password-reset-complete/',
#          auth_views.PasswordResetCompleteView.as_view(
#              template_name='password_reset_complete.html'
#          ),
#          name='password_reset_complete'),
# ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
