from rest_framework.serializers import ModelSerializer
from .models import Script

class ScriptSerializer(ModelSerializer):

    class Meta:
        model = Script
        exclude = ('id', 'video')
        
