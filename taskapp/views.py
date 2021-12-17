from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Task
from .forms import TaskForm


@login_required
def main(request):
    # Enable adding tasks to task list.
    the_tasks = Task.objects.filter(user=request.user.id).order_by('id')
    form = TaskForm()
    context = {'the_tasks': the_tasks, 'form': form}

    return render(request, 'index.html', context)


@require_POST
def add_task(request):

    form = TaskForm(data=request.POST)
    if form.is_valid():
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()

    return redirect('main')


def finished_task(request, task_id):

    task = Task.objects.get(pk=task_id)
    task.finished = True
    task.save()

    return redirect('main')


def delete_finished(request):

    Task.objects.filter(finished__exact=True).delete()

    return redirect('main')


def clear(request):

    Task.objects.all().delete()

    return redirect('main')
