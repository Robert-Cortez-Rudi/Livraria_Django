from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddBookForm
from .models import Book

def home(request):
    books = Book.objects.all()
    if request.method == "POST":
        username = request.POST["usuario"]
        password = request.POST["senha"]

        # Autenticação
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Login efetuado com sucesso!")
            return redirect("home")
        else:
            messages.error(request, "Erro na autenticação! Tente novamente!")
            return redirect("home")
    else:
        return render(request, "home.html", {"books": books})


def logout_user(request):
    logout(request)
    messages.success(request, "Logout efetuado com sucesso!")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Autenticação e login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Conta criada e login efetuado com sucesso!")
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "register.html", {"form": form})


def book_detail(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        return render(request, "book.html", {"book": book})
    else:
        messages.error(request, "Por favor, efetue o login!")
        return redirect("home")
    

def book_delete(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        book.delete()
        messages.success(request, "Livro deletado com sucesso!")
        return redirect("home")
    else:
        messages.error(request, "Por favor, efetue o login!")
        return redirect("home")


def book_add(request):
    form = AddBookForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Livro adicionado com sucesso!") 
                return redirect("home")   
        return render(request, "add_book.html", {"form": form})
    else:
        messages.error(request, "Por favor, efetue o login!")
        return redirect("home")
    

def book_update(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        form = AddBookForm(request.POST or None, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro atualizado com sucesso!")
            return redirect("home")
        return render(request, "update_book.html", {"form": form})
    else:
        messages.error(request, "Por favor, efetue o login para fazer a atualização!")
        return redirect("home")