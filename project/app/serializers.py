from django.db.models import Sum
from rest_framework import serializers

from .models import Product, Lesson, LessonView, Access, UserProfile


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    is_watched = serializers.SerializerMethodField()
    watched_at = serializers.SerializerMethodField()
    watching_duration = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ["title", "description", "video_link", "video_duration", "is_watched", "watched_at",
                  "watching_duration"]

    def get_is_watched(self, obj):
        data = self.context.get('data')
        try:
            lesson_info = LessonView.objects.get(user=data["user_id"], lesson=obj.id)
            return lesson_info.is_watched
        except:
            return "No data"

    def get_watched_at(self, obj):
        data = self.context.get('data')
        try:
            lesson_info = LessonView.objects.get(user=data["user_id"], lesson=obj.id)
            return lesson_info.watched_at
        except:
            return "No data"

    def get_watching_duration(self, obj):
        data = self.context.get('data')
        try:
            lesson_info = LessonView.objects.get(user=data["user_id"], lesson=obj.id)
            return lesson_info.watching_duration
        except:
            return "No data"


class StatisticSerializer(serializers.ModelSerializer):
    lessons_watched = serializers.SerializerMethodField()
    time_spent = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()
    product_share = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "title", "lessons_watched", "time_spent", "total_students", "product_share"]

    def get_lessons_watched(self, obj):
        lesson = LessonView.objects.filter(lesson__product=obj.id, is_watched=True)
        return lesson.count()

    def get_time_spent(self, obj):
        lesson = LessonView.objects.filter(lesson__product=obj.id)
        duration = lesson.aggregate(Sum('watching_duration'))
        return duration['watching_duration__sum']

    def get_total_students(self, obj):
        users = Access.objects.filter(product=obj.id, is_granted=True)
        total_students = users.count()
        return total_students

    def get_product_share(self, obj):
        users = Access.objects.filter(product=obj.id, is_granted=True).count()
        all_users = UserProfile.objects.all().count()
        return int(users/(all_users/100))

# class AccessSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Access
#         fields = "__all__"

# class LessonViewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LessonView
#         fields = "__all__"
#
#
# class OwnerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Owner
#         fields = "__all__"
#
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = "__all__"
