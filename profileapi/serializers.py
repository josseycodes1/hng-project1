from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True, max_length=255)
    stack = serializers.CharField(required=True, max_length=255)

class ProfileResponseSerializer(serializers.Serializer):
    status = serializers.CharField(required=True)
    user = UserSerializer(required=True)
    timestamp = serializers.CharField(required=True)
    fact = serializers.CharField(required=True, allow_blank=True)
    
    def validate_status(self, value):
        """Ensure status is always 'success'"""
        if value != "success":
            raise serializers.ValidationError("Status must be 'success'")
        return value