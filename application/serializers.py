from rest_framework import serializers
from .models import Training, Training_Type, CustomUser, Human_Gender


class TrainingSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    training_date = serializers.SerializerMethodField()
    training_leader_name = serializers.SerializerMethodField()
    training_types_dict = dict()
    training_types = serializers.SerializerMethodField()
    training_type = serializers.SerializerMethodField()
    def __init__(self, *args, **kwargs):
        super(TrainingSerializer, self).__init__(*args, **kwargs)
        temp = Training_Type.objects.all()
        for i in temp:
            self.training_types_dict.update({i.training_type_id: i.training_type})
    
    def get_full_name(self, obj):
        return obj.full_name
    
    def get_training_date(self, obj):
        return obj.training_date_
    
    def get_training_leader_name(self, obj):
        return obj.training_leader_name

    def get_training_types(self, obj):
        return self.training_types_dict.get(obj.training_type_id, "None")
    
    def get_training_type(self, obj):
        return obj.training_type

    class Meta:
        model = Training
        fields = "__all__"

class Training_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_Type
        fields = "__all__"


class Human_GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Human_Gender
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    #basic_info = serializers.SerializerMethodField()
    #full_name = serializers.SerializerMethodField()
    user_gender_name = serializers.SerializerMethodField()

    #def get_basic_info(self, obj):
    #    return obj.basic_info
    #
    #def get_full_name(self, obj):
    #    return obj.full_name
    #
    def get_user_gender_name(self, obj):
        return obj.user_gender.gender_name
    
    class Meta:
        model = CustomUser
        fields = "__all__"
