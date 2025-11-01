"""
URL patterns for RAG chatbot API
"""
from django.urls import path
from .views import (
    ChatbotQueryView,
    SuggestedQuestionsView,
    ChatbotHealthView
)

urlpatterns = [
    path('query/', ChatbotQueryView.as_view(), name='chatbot-query'),
    path('suggestions/', SuggestedQuestionsView.as_view(), name='chatbot-suggestions'),
    path('health/', ChatbotHealthView.as_view(), name='chatbot-health'),
]
