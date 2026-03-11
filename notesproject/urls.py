from django.contrib import admin
from django.urls import path
from notesapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),   

    path('', views.login_view, name='login'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

    path('notes/<int:section_id>/', views.view_notes, name='notes'),
    path('analyze/<int:note_id>/', views.analyze_pdf, name='analyze_pdf'),
    path('ask/', views.ask_question, name='ask_question'),
    path('analyze/<int:note_id>/', views.analyze_pdf, name='analyze_pdf'),
    path('ask/', views.ask_question, name='ask_question'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
