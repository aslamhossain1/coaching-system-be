from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Guardian, Student


class GuardianSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = Guardian
        fields = "__all__"
        read_only_fields = ("user",)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        email = validated_data["email"]
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password or User.objects.make_random_password(),
                first_name=validated_data.get("full_name", ""),
            )
        except IntegrityError as exc:
            raise serializers.ValidationError({"email": ["An account with this email already exists."]}) from exc
        validated_data["user"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if instance.user:
            if "email" in validated_data:
                instance.user.email = validated_data["email"]
                instance.user.username = validated_data["email"]
            if "full_name" in validated_data:
                instance.user.first_name = validated_data["full_name"]
            if password:
                instance.user.set_password(password)
            instance.user.save()
        return instance


class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ("user",)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        email = validated_data["email"]
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password or User.objects.make_random_password(),
                first_name=validated_data.get("full_name", ""),
            )
        except IntegrityError as exc:
            raise serializers.ValidationError({"email": ["An account with this email already exists."]}) from exc
        validated_data["user"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if instance.user:
            if "email" in validated_data:
                instance.user.email = validated_data["email"]
                instance.user.username = validated_data["email"]
            if "full_name" in validated_data:
                instance.user.first_name = validated_data["full_name"]
            if password:
                instance.user.set_password(password)
            instance.user.save()
        return instance
