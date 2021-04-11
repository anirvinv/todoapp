from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Todo
from django.db import IntegrityError

# Create your views here.

@login_required(login_url="login")
def index(request):
    # user = authenticate(username=request.user.username, password=request.user.password)

    if request.method=="POST":
        key = request.POST['key']
        request.user.todo.get(pk=key).delete()
        return HttpResponseRedirect(reverse('index'))

    user = request.user
    if user:
        # username = user.username
        # user = User.objects.get(username=username)
        # return HttpResponse(f"{user.todo.all()}")
        return render(request, 'todo/index.html', context={
            "todolist": user.todo.all()
        })
    # s = request.user.todo
    # return HttpResponse(f"{s.first()}")
    return render(request, 'todo/index.html')


def log_in(request):
    if request.method =="POST":
        

        username = request.POST['username']
        password = password=request.POST['password']

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return render(request, 'todo/login.html')
        # user = authenticate(username=username, password=password)

        if user.password == password:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse(f"{user.password}")
            # return render(request, 'todo/login.html')

    return render(request, 'todo/login.html')


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_passowrd = request.POST['confirm_password']
        
        if password == confirm_passowrd:
            try:
                user = User.objects.create(username=username, password=password)
            except IntegrityError:
                context = {
                "message":"Username is already taken."
                }
                return render(request, 'todo/signup.html', context=context)
            return HttpResponseRedirect(reverse('login'))
        else:
            context = {
                "message":"Passwords did not match, please make sure that both fields have the same text."
            }
            return render(request, 'todo/signup.html', context=context)

    return render(request, 'todo/signup.html', context={
        'message':""
    })


@login_required(login_url='login')
def add(request):
    class TodoForm(forms.Form):
        todo = forms.CharField(required=True)
    
    if request.method=="POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.cleaned_data['todo']
            Todo.objects.create(user=request.user, content=todo)

        else:
            return render(request, 'todo/add.html', context={
                "form": form
            })
    
    context={"form":TodoForm()}
    return render(request, 'todo/add.html',context=context)