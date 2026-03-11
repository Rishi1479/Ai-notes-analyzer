from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from .models import Section, Note

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:

            login(request,user)

            if user.is_superuser:
                return redirect('admin_dashboard')

            else:
                return redirect('student_dashboard')

    return render(request,'login.html')
def admin_dashboard(request):

    sections = Section.objects.all()

    return render(request,'admin_dashboard.html',{'sections':sections})
def student_dashboard(request):

    sections = Section.objects.all()

    return render(request,'student_dashboard.html',{'sections':sections})
def view_notes(request,section_id):

    notes = Note.objects.filter(section_id=section_id)

    return render(request,'notes.html',{'notes':notes})
from django.http import JsonResponse
from .pdf_ai import extract_text, split_text, create_embeddings, answer_question
from .models import Note


pdf_store = {}


def analyze_pdf(request, note_id):

    note = Note.objects.get(id=note_id)

    pdf_path = note.file.path

    text = extract_text(pdf_path)

    chunks = split_text(text)

    embeddings = create_embeddings(chunks)

    pdf_store[note_id] = (chunks, embeddings)

    return render(request, "chat.html", {"note_id": note_id})


def ask_question(request):

    question = request.POST.get("question")
    note_id = int(request.POST.get("note_id"))

    chunks, embeddings = pdf_store[note_id]

    answer = answer_question(question, chunks, embeddings)

    return JsonResponse({"answer": answer})
from django.http import JsonResponse
from .models import Note
from .ollama_ai import ask_llama

pdf_context = {}
def analyze_pdf(request, note_id):

    note = Note.objects.get(id=note_id)

    pdf_path = note.file.path

    text = extract_text(pdf_path)

    pdf_context[note_id] = text

    return render(request, "chat.html", {"note_id": note_id})
def ask_question(request):

    question = request.POST.get("question")
    note_id = int(request.POST.get("note_id"))

    context = pdf_context.get(note_id)

    answer = ask_llama(question, context)

    return JsonResponse({"answer": answer})