from rest_framework import serializers
from .models import ARScene, ARObject


class ARObjectSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ARObject
        fields = [
            "id",
            "name",
            "model_url",
            "rotation_deg",
            "scale",
            "info",
            "image",
            "offset_x",
            "offset_y",
            "offset_z",
            "description",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class ARSceneSerializer(serializers.ModelSerializer):
    marker_image = serializers.SerializerMethodField()
    model_url = serializers.SerializerMethodField()
    objects = ARObjectSerializer(many=True, read_only=True)  # Include child objects

    class Meta:
        model = ARScene
        fields = [
            "id",
            "name",
            "description",
            "latitude",
            "longitude",
            "marker_image",
            "model_url",
            "objects",
        ]

    def get_marker_image(self, obj):
        request = self.context.get("request")
        if obj.marker_image:
            return request.build_absolute_uri(obj.marker_image.url)
        return None

    def get_model_url(self, obj):
        request = self.context.get("request")
        if obj.model_file:
            return request.build_absolute_uri(obj.model_file.url)
        return None
