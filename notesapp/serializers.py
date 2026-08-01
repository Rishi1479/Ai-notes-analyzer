from rest_framework import serializers
from .models import User, Section, Note


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = ['id', 'username', 'role']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name']


class NoteSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'title', 'section', 'file', 'file_url', 'uploaded_by']
        read_only_fields = ['id', 'uploaded_by']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class NoteUploadSerializer(serializers.ModelSerializer):
    """Serializer for teachers uploading notes."""

    class Meta:
        model = Note
        fields = ['id', 'title', 'section', 'file']
        read_only_fields = ['id']


class AskQuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=2000)
    note_id = serializers.IntegerField()
