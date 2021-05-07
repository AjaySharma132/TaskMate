from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TaskList
from .forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def todolist(request):
    if request.method == 'POST':
        form=TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).owner = request.user
            form.save()
            messages.success(request, "New Task Added!!")
        return redirect('todolist')
    else:
        all_tasks=TaskList.objects.filter(owner=request.user)
        paginator=Paginator(all_tasks,11)
        page=request.GET.get('pg')
        all_tasks=paginator.get_page(page)
        return render(request, 'todolist.html', {'Task': all_tasks})

def about(request):
    context={
        "about": "This is about page",
    }
    return render(request, 'about.html', context)

def contact(request):
    context={
        "contact": "This is contact page",
    }
    return render(request, 'contact.html', context)

@login_required
def delete_task(request, task_id):
    task=TaskList.objects.get(id=task_id)
    task.delete()
    return redirect('todolist')

@login_required
def edit_task(request, task_id):
    if request.method == 'POST':
        taskobj=TaskList.objects.get(id=task_id)
        form=TaskForm(request.POST or None, instance=taskobj)
        if form.is_valid():
            form.save()
            messages.success(request, "Task Edited Successfully!!")
        return redirect('todolist')
    else:
        taskobj=TaskList.objects.get(id=task_id)
        return render(request, 'edit.html', {'taskobj': taskobj})

@login_required
def completed(request, task_id):
    taskobj=TaskList.objects.get(id=task_id)
    if request.user == taskobj.owner:
        taskobj.status=True
        taskobj.save()
        try:    
            return redirect(request.META.get('HTTP_REFERER'))
        except:
            return redirect('todolist')
    else:
        messages.error(request, 'Access Denied')
        return redirect('todolist')
    

@login_required
def pending(request, task_id):
    taskobj=TaskList.objects.get(id=task_id)
    if request.user == taskobj.owner:
        taskobj.status=False
        taskobj.save()
        try:    
            return redirect(request.META.get('HTTP_REFERER'))
        except:
            return redirect('todolist')
    else:
        messages.error(request, 'Access Denied')
        return redirect('todolist')
    
    
        

def index(request):
    context={
        "Welcome": "Welcome Home page"
    }
    return render(request, 'index.html', context)
