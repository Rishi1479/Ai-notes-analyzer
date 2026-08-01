from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from notesapp import views
from notesapp import api_views

urlpatterns = [
    # ── Django Admin ──
    path('admin/', admin.site.urls),

    # ── Template-based views (session auth) ──
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('upload_note/', views.upload_note, name='upload_note'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('notes/<int:section_id>/', views.view_notes, name='notes'),
    path('analyze/<int:note_id>/', views.analyze_pdf, name='analyze_pdf'),
    path('ask/', views.ask_question, name='ask_question'),

    # ── JWT Authentication ──
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ── API Views (JWT auth + permissions) ──
    path('api/me/', api_views.CurrentUserAPI.as_view(), name='api_me'),
    path('api/sections/', api_views.SectionListAPI.as_view(), name='api_sections'),
    path('api/notes/<int:section_id>/', api_views.NoteListAPI.as_view(), name='api_notes'),
    path('api/notes/upload/', api_views.UploadNoteAPI.as_view(), name='api_upload_note'),
    path('api/notes/delete/<int:note_id>/', api_views.DeleteNoteAPI.as_view(), name='api_delete_note'),
    path('api/analyze/<int:note_id>/', api_views.AnalyzeNoteAPI.as_view(), name='api_analyze'),
    path('api/ask/', api_views.AskQuestionAPI.as_view(), name='api_ask'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
