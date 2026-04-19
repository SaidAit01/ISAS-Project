from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Retrieve the first group assigned to the user and inject it as the 'role'
        if user.groups.exists():
            token['role'] = user.groups.first().name
        else:
            token['role'] = 'Unassigned'
            
        return token