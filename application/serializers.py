from rest_framework import serializers
from .models import Training


class TrainingSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    training_date = serializers.SerializerMethodField()
    training_leader_name = serializers.SerializerMethodField()
    def get_full_name(self, obj):
        return obj.full_name
    
    def get_training_date(self, obj):
        return obj.training_date_
    
    def get_training_leader_name(self, obj):
        return obj.training_leader_name

    class Meta:
        model = Training
        fields = "__all__"

