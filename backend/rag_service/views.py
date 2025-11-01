"""
API views for RAG chatbot
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .chatbot import PortfolioRAGChatbot
from .serializers import (
    ChatQuerySerializer,
    ChatResponseSerializer,
    SuggestedQuestionsSerializer
)

# Initialize chatbot (singleton pattern)
chatbot = None

def get_chatbot():
    """Get or create chatbot instance"""
    global chatbot
    if chatbot is None:
        chatbot = PortfolioRAGChatbot()
    return chatbot

class ChatbotQueryView(APIView):
    """
    API endpoint for chatbot queries
    Accepts questions and returns AI-generated answers using RAG
    """

    def post(self, request):
        """Handle chatbot query"""
        # Validate input
        serializer = ChatQuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract parameters
        question = serializer.validated_data['question']
        k = serializer.validated_data.get('k', 5)
        include_sources = serializer.validated_data.get('include_sources', True)

        try:
            # Get chatbot and query
            bot = get_chatbot()
            response = bot.query(
                question=question,
                k=k,
                include_sources=include_sources
            )

            # Return response
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SuggestedQuestionsView(APIView):
    """
    API endpoint to get suggested questions
    """

    def get(self, request):
        """Return suggested questions"""
        bot = get_chatbot()
        questions = bot.get_suggested_questions()

        return Response(
            {"questions": questions},
            status=status.HTTP_200_OK
        )

class ChatbotHealthView(APIView):
    """
    Health check endpoint for chatbot service
    """

    def get(self, request):
        """Check if chatbot is initialized and vector store has data"""
        try:
            bot = get_chatbot()
            doc_count = bot.vector_store.count()

            return Response({
                "status": "healthy",
                "vector_store_documents": doc_count,
                "ready": doc_count > 0
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "unhealthy",
                "error": str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
