from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Section, Note
from .rag import index_document, retrieve_chunks
from .ollama_ai import ask_llama


def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Route based on role
            if user.role == 'admin' or user.is_superuser:
                return redirect('admin_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            error = "Invalid username or password."
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def admin_dashboard(request):
    if request.user.role not in ('admin',) and not request.user.is_superuser:
        return redirect('login')
    sections = Section.objects.all()
    return render(request, 'admin_dashboard.html', {'sections': sections})


@login_required(login_url='login')
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('login')
    sections = Section.objects.all()
    notes = Note.objects.filter(uploaded_by=request.user)
    return render(request, 'teacher_dashboard.html', {
        'sections': sections,
        'notes': notes,
    })


@login_required(login_url='login')
def upload_note(request):
    """Handle note upload from teacher dashboard form."""
    if request.user.role != 'teacher':
        return redirect('login')
    if request.method == "POST":
        title = request.POST.get('title')
        section_id = request.POST.get('section')
        file = request.FILES.get('file')
        if title and section_id and file:
            note = Note(
                title=title,
                section_id=section_id,
                file=file,
                uploaded_by=request.user,
            )
            note.save()
    return redirect('teacher_dashboard')


@login_required(login_url='login')
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('login')
    sections = Section.objects.all()
    return render(request, 'student_dashboard.html', {'sections': sections})


@login_required(login_url='login')
def view_notes(request, section_id):
    notes = Note.objects.filter(section_id=section_id)
    return render(request, 'notes.html', {'notes': notes})


@login_required(login_url='login')
def analyze_pdf(request, note_id):
    note = Note.objects.get(id=note_id)
    pdf_path = note.file.path
    try:
        index_document(note_id, pdf_path)
    except ValueError as e:
        return render(request, 'chat.html', {
            'note_id': note_id,
            'error': str(e),
        })
    return render(request, 'chat.html', {'note_id': note_id})


@login_required(login_url='login')
def ask_question(request):
    question = request.POST.get("question")
    note_id = int(request.POST.get("note_id"))
    chunks = retrieve_chunks(note_id, question)
    context = "\n\n".join(chunks)
    answer = ask_llama(question, context, model="gemma4:e2b")
    return JsonResponse({"answer": answer})