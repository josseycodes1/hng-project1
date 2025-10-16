from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from datetime import datetime
import logging

from .serializers import ProfileResponseSerializer, UserSerializer

logger = logging.getLogger(__name__)

class ProfileView(APIView):
    def get(self, request):
        try:
            # Fetch cat fact
            cat_fact = self.get_cat_fact()
            
            
            user_data = {
                "email": "adewumijosephine1@gmail.com",  
                "name": "Adewumi Josephine",   
                "stack": "Python/Django/DRF" 
            }
            
            # Prepare the response data
            response_data = {
                "status": "success",
                "user": user_data,
                "timestamp": datetime.utcnow().isoformat() + 'Z',
                "fact": cat_fact
            }
            
            # Use serializer to validate our data
            serializer = ProfileResponseSerializer(data=response_data)
            
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            else:
                # If serializer fails, return the data anyway (but log the error)
                logger.error(f"Serializer errors: {serializer.errors}")
                return Response(response_data, status=status.HTTP_200_OK)
                
        except Exception as e:
            # Fallback if everything fails
            fallback_data = {
                "status": "success",
                "user": {
                    "email": "your-email@gmail.com",
                    "name": "Your Name", 
                    "stack": "Python/Django/DRF"
                },
                "timestamp": datetime.utcnow().isoformat() + 'Z',
                "fact": "Cats are napping - no facts right now!"
            }
            return Response(fallback_data, status=status.HTTP_200_OK)
    
    def get_cat_fact(self):
        try:
            response = requests.get('https://catfact.ninja/fact', timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('fact', 'No fact available') or 'No fact available'  # Added fallback
        except:
            return "Unable to fetch cat fact at the moment"