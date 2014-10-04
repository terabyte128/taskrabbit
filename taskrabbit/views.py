from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User

from taskrabbit.models import Task, Note, Team, UserProfile, Status


# Create your views here.
def index(request):

    context = {
        'page': "index"
    }

    context['tasks'] = Task.objects.filter(owner=request.user)

    add_context(context, request)

    return render(request, 'taskrabbit/index.html', context)


def add_context(context, request):
    try:
        context['teams'] = Team.objects.all()
        context['user'] = request.user
    except Team.DoesNotExist:
        pass

    return context


def teams(request, team_id):

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