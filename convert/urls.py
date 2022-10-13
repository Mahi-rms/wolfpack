from django.urls import path
from . import views
urlpatterns = [
    path('upload-image/', views.Upload.as_view()),
]