from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import dashboard, start_assessment, assessment_result
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
  #  path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
     path('assessment/', start_assessment, name='start_assessment'),
    path('assessment/result/', assessment_result, name='assessment_result'),
     path('therapy/', views.therapy_plan, name='therapy_plan'),
    path('therapy/day/<int:day_number>/', views.start_therapy_day, name='start_therapy_day'),
    path('voice-assistant/', views.voice_assistant, name='voice_assistant'),
    path('assistant/chat/', views.assistant_chat, name='assistant_chat'),
   # path('assistant/speak/', views.generate_speech, name='assistant_speak'),
    path('assistant/speak/', views.generate_speech, name='generate_speech'),
    path('experts/', views.expert_list, name='expert_list'),
    path('expert/signin/', views.expert_signin, name='expert_signin'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)