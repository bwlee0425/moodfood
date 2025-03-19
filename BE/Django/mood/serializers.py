from rest_framework import serializers
from .models import Mood

class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['id', 'mood', 'created_at']