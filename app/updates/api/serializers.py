from rest_framework import serializers

from updates.models import (
    ProfileUpdate,
    MeasuresUpdate,
    GalleryUpdate,
    ProfilePictureUpdate,
    CoverPictureUpdate,
)


class OutputProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUpdate
        fields = ("id", "bio", "accept", "decline", "message")


class InputProfileUpdateSerializer(serializers.Serializer):
    bio = serializers.CharField(max_length=500)


class OutputMeasuresUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasuresUpdate
        fields = (
            "id",
            "height",
            "waist",
            "bust",
            "shoulders",
            "hips",
            "weight",
            "shoe_size",
            "hair",
            "eyes",
            "accept",
            "decline",
            "message",
        )


class InputMeasuresUpdateSerializer(serializers.Serializer):
    height = serializers.DecimalField(max_digits=5, decimal_places=2)
    waist = serializers.DecimalField(max_digits=5, decimal_places=2)
    bust = serializers.IntegerField()
    shoulders = serializers.IntegerField()
    hips = serializers.IntegerField()
    weight = serializers.IntegerField()
    shoe_size = serializers.IntegerField()
    hair = serializers.CharField(max_length=100)
    eyes = serializers.CharField(max_length=100)


class OutputGalleryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryUpdate
        fields = ("id", "image", "accept", "decline", "message", "related_photo")


class InputGalleryUpdateSerializer(serializers.Serializer):
    image = serializers.ImageField()


class OutputProfilePictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePictureUpdate
        fields = ("id", "image", "accept", "decline", "message")


class InputProfilePictureUpdateSerializer(serializers.Serializer):
    image = serializers.ImageField()


class OutputCoverPictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverPictureUpdate
        fields = ("id", "image", "accept", "decline", "message")


class InputCoverPictureUpdateSerializer(serializers.Serializer):
    image = serializers.ImageField()
