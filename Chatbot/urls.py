from django.contrib import admin
from django.urls import path
from app_Chatbot import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Chatbot, name="Chatbot"),
    path('upload-arquivo/', views.upload_arquivo, name='upload_arquivo'),
    path('consulta/', views.consulta, name='consulta'),  # Nova rota para consulta
]
