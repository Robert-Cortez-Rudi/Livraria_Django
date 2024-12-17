from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

def home(request):
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
        return render(request, "home.html")


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
