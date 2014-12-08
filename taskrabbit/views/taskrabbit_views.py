import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
import datetime

from taskrabbit.models import Task, Note, Team, UserProfile, Status

# Create your views here.


def index(request):

    if request.user.is_authenticated():
        context = {
            'page': 'index'
        }

        add_context(context, request)

        statuses = Status.objects.all()

        tiny_package = []

        for a_status in statuses:
            tiny_package.append({
                'name': a_status.name,
                'count': Task.objects.filter(owner=request.user, status=a_status).count()
            })

        context['user_statuses'] = tiny_package


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


@login_required
def my_tasks(request):
    context = {
        'page': 'my_tasks',
        'tasks': Task.objects.filter(owner=request.user),
        'hide_statuses': Status.objects.filter(show_in_table=False)
    }

    add_context(context, request)

    return render(request, 'taskrabbit/my_tasks.html', context)


@login_required
def log_out(request):
    logout(request)
    messages.success(request, "Signed out successfully.")
    return render(request, 'taskrabbit/login.html')


def add_context(context, request):
    try:
        context['teams'] = Team.objects.all()
        context['statuses'] = Status.objects.all()
        context['user'] = request.user
    except Team.DoesNotExist:
        pass

    return context


@login_required
def teams(request, team_id=None):

    if not team_id:
        raise Http404

    context = {
        'page': 'teams',
        'hide_statuses': Status.objects.filter(show_in_table=False)
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
def statuses(request, status_id=None):

    if not status_id:
        raise Http404

    context = {
        'page': 'statuses',
        'hide_statuses': Status.objects.filter(show_in_table=False)
    }

    try:
        status = Status.objects.get(id=status_id)
        context['status'] = status
    except Status.DoesNotExist:
        raise Http404

    try:
        context['tasks'] = Task.objects.filter(status=status)
    except Task.DoesNotExist:
        context['errors'] = "No tasks found."

    add_context(context, request)

    return render(request, 'taskrabbit/statuses.html', context)


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


@login_required
def get_users(request):
    users = User.objects.filter(is_active=True)

    json_user = []

    for a_user in users:
        user_package = {
            'value': a_user.id,
            'text': a_user.first_name
        }
        json_user.append(user_package)

    return HttpResponse(json.dumps(json_user), content_type='application/json')


@login_required
def update_task(request):
    name = request.POST['name']
    pk = request.POST['pk']
    value = request.POST['value']

    try:
        task = Task.objects.get(id=pk)

        if name == "owner":
            value_as_object = User.objects.get(id=value)
            note_description = "Owner changed to " + value_as_object.first_name + "."

        elif name == "status":
            value_as_object = Status.objects.get(id=value)
            note_description = "Status changed to " + str(value_as_object).lower() + "."

        else:
            value_as_object = value
            note_description = None

        if note_description is not None:
            note_update = Note(task=task, user=request.user, status=task.status, content=note_description,
                               timestamp=datetime.datetime.now(), automatic_note=True)
            note_update.save()

        setattr(task, name, value_as_object)
        task.save()

    except Task.DoesNotExist:
        raise Http404

    return HttpResponse(status=200)


@login_required
def add_note(request):
    task_id = request.POST['task_id']
    content = request.POST['content']

    task = Task.objects.get(id=task_id)

    new_note = Note(task=task, user=request.user, status=task.status, content=content, timestamp=datetime.datetime.now())

    new_note.save()

    task.last_worked_on = datetime.datetime.now()

    task.save()

    return HttpResponseRedirect(reverse('taskrabbit:view_task') + task_id)


@login_required
def search(request):
    query = request.GET['query']

    context = {
        'page': 'search',
        'query': query,
    }

    results = Task.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context['tasks'] = results

    add_context(context, request)

    return render(request, 'taskrabbit/search_results.html', context)


@login_required
def all_tasks(request):

    context = {
        'page': 'all_tasks',
        'hide_statuses': Status.objects.filter(show_in_table=False)
    }

    try:
        context['tasks'] = Task.objects.all()
    except Task.DoesNotExist:
        context['errors'] = "No tasks found."

    add_context(context, request)

    return render(request, 'taskrabbit/all_tasks.html', context)