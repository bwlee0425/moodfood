from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Mood
from .serializers import MoodEntrySerializer

@api_view(['POST'])
def mood_create(request):
    mood = request.data.get('mood')
    
    if not mood:
        return Response({"error": "mood 값이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = MoodEntrySerializer(data={'mood': mood})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
