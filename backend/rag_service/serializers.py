"""
Serializers for RAG chatbot API
"""
from rest_framework import serializers

class ChatQuerySerializer(serializers.Serializer):
    """Serializer for chatbot query requests"""
    question = serializers.CharField(
        max_length=500,
        help_text="Question to ask the chatbot"
    )
    k = serializers.IntegerField(
        default=5,
        min_value=1,
        max_value=10,
        help_text="Number of context documents to retrieve"
    )
    include_sources = serializers.BooleanField(
        default=True,
        help_text="Include source documents in response"
    )

class SourceSerializer(serializers.Serializer):
    """Serializer for source document metadata"""
    source = serializers.CharField()
    category = serializers.CharField()
    chunk_id = serializers.IntegerField()
    relevance_score = serializers.FloatField()

class ChatResponseSerializer(serializers.Serializer):
    """Serializer for chatbot response"""
    answer = serializers.CharField()
    context_used = serializers.IntegerField()
    sources = SourceSerializer(many=True, required=False)

class SuggestedQuestionsSerializer(serializers.Serializer):
    """Serializer for suggested questions"""
    questions = serializers.ListField(
        child=serializers.CharField()
    )
