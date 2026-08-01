from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Section, Note
from .serializers import (
    SectionSerializer, NoteSerializer, NoteUploadSerializer, AskQuestionSerializer, UserSerializer
)
from .permissions import IsTeacher, IsStudent, IsTeacherOrAdmin, IsOwner
from .rag import index_document, retrieve_chunks
from .ollama_ai import ask_llama


class CurrentUserAPI(APIView):
    """Return the current authenticated user's info."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class SectionListAPI(APIView):
    """List all sections. Any authenticated user can access."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sections = Section.objects.all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)


class NoteListAPI(APIView):
    """List notes for a section. Any authenticated user can access."""
    permission_classes = [IsAuthenticated]

    def get(self, request, section_id):
        notes = Note.objects.filter(section_id=section_id)
        serializer = NoteSerializer(notes, many=True, context={'request': request})
        return Response(serializer.data)


class UploadNoteAPI(APIView):
    """Upload a note. Only teachers can upload."""
    permission_classes = [IsTeacher]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = NoteUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(
                {"msg": "Note uploaded successfully", "note": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteNoteAPI(APIView):
    """Delete a note. Only the teacher who uploaded it can delete."""
    permission_classes = [IsTeacher, IsOwner]

    def delete(self, request, note_id):
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, note)
        note.file.delete()
        note.delete()
        return Response({"msg": "Note deleted"}, status=status.HTTP_200_OK)


class AnalyzeNoteAPI(APIView):
    """Index a PDF for RAG. Only students can analyze."""
    permission_classes = [IsStudent]

    def post(self, request, note_id):
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

        index_document(note_id, note.file.path)
        return Response({"msg": "PDF indexed successfully", "note_id": note_id})


class AskQuestionAPI(APIView):
    """Ask a question about an indexed note. Only students can ask."""
    permission_classes = [IsStudent]

    def post(self, request):
        serializer = AskQuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data['question']
            note_id = serializer.validated_data['note_id']

            chunks = retrieve_chunks(note_id, question)
            context = "\n\n".join(chunks)
            answer = ask_llama(question, context, model="gemma4:e2b")

            return Response({"answer": answer})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
