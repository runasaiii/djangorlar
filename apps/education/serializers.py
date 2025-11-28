# Python modules
from rest_framework import serializers

# Project modules
from apps.education.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model."""
    owner = serializers.StringRelatedField(read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'is_active', 'owner', 'created_at', 'deleted_at', 'updated_at', 'lessons_count']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at', 'owner', 'lessons_count']

    def get_lessons_count(self, obj):
        """Get count of non-deleted lessons for the course."""
        return obj.lessons.filter(deleted_at__isnull=True).count()

    def create(self, validated_data):
        """Override create to set the owner from request user."""
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)
    

class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lesson model."""
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'indentation', 'order', 'is_published', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['order', 'created_at', 'updated_at', 'deleted_at']

    def validate_indentation(self, value):
        """Validate that indentation is between 0 and 5."""
        if value is None:
            return 0
        if value < 0 or value > 5:
            raise serializers.ValidationError("Indentations should be between 0 and 5")
        return value
    
    def create(self, validated_data):
        """Override create to check course ownership."""
        request = self.context['request']
        course = validated_data.get('course')
        if course.owner.id != request.user.id:
            raise serializers.ValidationError("You must be the owner of course to add lessons")
        return super().create(validated_data)
    