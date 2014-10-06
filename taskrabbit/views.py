import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User

from taskrabbit.models import Task, Note, Team, UserProfile, Status


# Create your views here.
def index(request):

    if request.user.is_authenticated():

        context = {
            'page': 'index',
            'tasks': Task.objects.filter(owner=request.user)
        }

        add_context(context, request)

        return render(request, 'taskrabbit/index.html', context)


    elif 'username' and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('taskrabbit:index'))
            else:
                messages.error(request, "Your account has been deactivated.")
        else:
            messages.error(request, "Account not found. Make sure your credentials are entered correctly.")

        return render(request, 'taskrabbit/login.html')

    else:
        return render(request, 'taskrabbit/login.html')


def log_out(request):
    logout(request)
    messages.success(request, "Signed out successfully.")
    return render(request, 'taskrabbit/login.html')


def add_context(context, request):
    try:
        context['teams'] = Team.objects.all()
        context['user'] = request.user
    except Team.DoesNotExist:
        pass

    return context


@login_required
def teams(request, team_id=None):

    if not team_id:
        raise Http404

    context = {
        'page': 'teams'
    }

    try:
        team = Team.objects.get(id=team_id)
        context['team'] = team
    except Team.DoesNotExist:
        raise Http404

    try:
        context['tasks'] = Task.objects.filter(team=team)
    except Task.DoesNotExist:
        context['errors'] = "No tasks found."

    add_context(context, request)

    return render(request, 'taskrabbit/teams.html', context)


@login_required
def add_task(request):

    if 'name' and 'team' in request.POST:
        name = request.POST['name']
        description = request.POST['description']
        due_date = request.POST['due_date']
        team = request.POST['team']
        owner = request.POST['owner']

        new_task = Task(name=name, description=description, team=Team.objects.get(id=team), status=Status.objects.get(id=1))

        if not owner == "":
            new_task.owner = User.objects.get(id=owner)

        if not due_date == "":
            new_task.due_date = due_date

        new_task.save()

        return HttpResponseRedirect(reverse('taskrabbit:index'))

    context = {
        'page': 'add_task',
        'users': User.objects.all()
    }

    add_context(context, request)

    return render(request, 'taskrabbit/add_task.html', context)


@login_required
def claim_task(request):

    if 'task_id' in request.POST:
        task_id = request.POST['task_id']

        try:
            task = Task.objects.get(id=task_id)
            task.owner = request.user
            task.save()
        except Task.DoesNotExist:
            raise Http404

        return HttpResponseRedirect(reverse('taskrabbit:index'))

    raise Http404


@login_required
def view_task(request, task_id=None):
    if not task_id:
        raise Http404

    try:
        task = Task.objects.get(id=task_id)



    except Task.DoesNotExist:
        raise Http404

    context = {
        'task': task,
        'notes': Note.objects.filter(task=task).order_by('-timestamp')
    }

    add_context(context, request)

    return render(request, 'taskrabbit/view_task.html', context)


@login_required
def get_statuses(request):
    status = Status.objects.all()

    json_status = []

    for a_status in status:
        status_package = {
            'value': a_status.id,
            'text': a_status.name
        }
        json_status.append(status_package)

    return HttpResponse(json.dumps(json_status), content_type='application/json')