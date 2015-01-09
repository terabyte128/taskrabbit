import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.utils import timezone
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from datetime import datetime
import local_settings
from send_sms.models import PhoneNumber, Carrier
from send_sms.send_sms import send_text_message, has_phone_number

from taskrabbit.models import Task, Note, Team, Status, TimeLog, AccountCreationID, PasswordResetID, Theme, UserProfile
from taskrabbit.utils.time_utils import get_total_time, strfdelta

# Create your views here.
TABLE_ENTRIES_PER_PAGE = 10


def show_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('taskrabbit:index'))
    else:
        context = {}
        if 'next' in request.GET:
            redirect = request.GET['next']
            context['redirect'] = redirect

        return render(request, 'taskrabbit/login.html', context)


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

        # find if they're timed in
        try:
            raw_time_logs = TimeLog.objects.filter(user=request.user, valid=True)
            if len(raw_time_logs) == 0:
                currently_timed_in = False
                context['currently_timed_in'] = False
                context['grand_total_time'] = '00:00'
            else:
                latest_log = raw_time_logs.latest('id')
                grand_total_time = get_total_time(raw_time_logs)
                if not latest_log.exit_time:
                    current_time_length = timezone.now() - latest_log.entry_time
                    currently_timed_in = True
                else:
                    currently_timed_in = False
                context['currently_timed_in'] = currently_timed_in
                context['grand_total_time'] = strfdelta(grand_total_time, "{HH}:{MM}")

            if currently_timed_in:
                context['current_time_length'] = int(current_time_length.total_seconds())
            else:
                context['current_time_length'] = 0
        except TimeLog.DoesNotExist:
            context = {
                'currently_timed_in': False,
                'grand_total_time': '00:00',
                'current_time_length': 0
            }

        return render(request, 'taskrabbit/index.html', context)

    elif 'username' and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if 'redirect' in request.POST:
                    return HttpResponseRedirect(request.POST['redirect'])
                else:
                    return HttpResponseRedirect(reverse('taskrabbit:index'))
            else:
                messages.error(request, "Your account has been deactivated.")
        else:
            messages.error(request, "Account not found. Make sure your credentials are entered correctly.")

        return HttpResponseRedirect(reverse('taskrabbit:login'))

    else:
        return HttpResponseRedirect(reverse('taskrabbit:login'))


@login_required
def my_tasks(request):

    tasks = Task.objects.filter(owner=request.user, status__show_in_table=True)

    context = {
        'page': 'my_tasks',
        'tasks': tasks,
        'events': format_tasks_as_events(tasks),
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
        # 'hide_statuses': Status.objects.filter(show_in_table=False)
    }

    try:
        team = Team.objects.get(id=team_id)
        context['team'] = team
    except Team.DoesNotExist:
        raise Http404

    try:
        tasks = Task.objects.filter(team=team, status__show_in_table=True)
        context['tasks'] = tasks
        context['events'] = format_tasks_as_events(tasks)

    except Task.DoesNotExist:
        context['errors'] = "No tasks found."

    add_context(context, request)

    return render(request, 'taskrabbit/teams.html', context)


@login_required
def statuses(request, status_id=None, page="1"):

    if not status_id:
        raise Http404

    context = {
        'page': 'statuses',
        # 'hide_statuses': Status.objects.filter(show_in_table=False),
        'status_id': status_id
    }

    try:
        status = Status.objects.get(id=status_id)
        context['status'] = status
    except Status.DoesNotExist:
        raise Http404

    try:
        page = int(page)
        begin_entries = TABLE_ENTRIES_PER_PAGE * (page-1)
        end_entries = TABLE_ENTRIES_PER_PAGE * page
        if len(Task.objects.filter(status=status)) <= end_entries:
            next_page = 0
        else:
            next_page = page+1
        prev_page = page-1
        context['next_page'] = next_page
        context['prev_page'] = prev_page
        context['page_num'] = page
        context['tasks'] = Task.objects.filter(status=status)[begin_entries:end_entries]
    except Task.DoesNotExist:
        context['errors'] = "No tasks found."

    add_context(context, request)

    return render(request, 'taskrabbit/statuses.html', context)


@login_required
def add_task(request):

    if 'name' and 'team' in request.POST:
        name = request.POST['name']
        description = request.POST['description']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        team = request.POST['team']
        owner = request.POST['owner']

        new_task = Task(name=name, description=description,
                        team=Team.objects.get(id=team), status=Status.objects.get(id=1), created_by=request.user)

        if not owner == "":
            new_task.owner = User.objects.get(id=owner)

        if not start_date == "":
            new_task.start_date = start_date

        new_task.end_date = end_date

        new_task.save()

        if 'email' in request.POST and new_task.owner is not None:
            print('Sending email to %s.' % new_task.owner.email)

            email_url = local_settings.SITE_URL + reverse('taskrabbit:view_task', kwargs={'task_id': new_task.id})

            plaintext_email_content = format("Greetings,\n" \
                                                "\n" \
                                                "You have been assigned a new task on TaskRabbit by %s.\n" \
                                                "Name: %s\n" \
                                                "More info at: %s\n" \
                                                "\n" \
                                                "Sincerely,\n" \
                                                "The Rabbit" % (request.user.get_full_name(), new_task.name, email_url))

            html_email_content = format("Greetings,<br>" \
                                        "<br>" \
                                        "You have been assigned a new task on TaskRabbit by %s.<br>" \
                                        "Name: %s<br>" \
                                        "<a href='%s' target='_blank'>Click here for more info!</a><br>" \
                                        "<br>" \
                                        "Sincerely,<br>" \
                                        "The Rabbit" % (request.user.get_full_name(), new_task.name, email_url))

            new_task.owner.email_user("New task on TaskRabbit", plaintext_email_content, html_message=html_email_content)

        if 'add' in request.POST:
            return HttpResponseRedirect(reverse('taskrabbit:view_task', args=(new_task.id,)))
        else:
            return render(request, 'taskrabbit/add_task.html', {'page': 'add_task', 'users': User.objects.all(), 'teams': Team.objects.all()})

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

        return HttpResponseRedirect(reverse('taskrabbit:my_tasks'))

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
        'notes': Note.objects.filter(task=task).order_by('-timestamp'),
        'has_phone_number': has_phone_number(task.owner)
    }

    add_context(context, request)

    return render(request, 'taskrabbit/view_task.html', context)


@login_required
def user_profile(request, user_id=None):
    if not user_id:
        raise Http404

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404

    try:
        tasks = Task.objects.filter(owner=user_id, status__show_in_table=True)
    except Task.DoesNotExist:
        tasks = []

    statuses = Status.objects.all()

    tiny_package = []

    for a_status in statuses:
        tiny_package.append({
            'name': a_status.name,
            'id': a_status.id,
            'count': Task.objects.filter(owner=request.user, status=a_status).count()
        })
    
    events = format_tasks_as_events(tasks)

    context = {
        'user_statuses': tiny_package,
        'user': user,
        'tasks': tasks,
        'events': events
    }

    return render(request, 'taskrabbit/user_profile.html', context)


@login_required
def user_status(request, user_id=None, status_id=None):
    if not user_id:
        raise Http404

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404

    try:
        status = Status.objects.get(id=status_id)
    except Statue.DoesNotExist:
        raise Http404

    try:
        tasks = Task.objects.filter(owner=user_id, status=status_id)
    except Task.DoesNotExist:
        tasks = []

    context = {
        'status': status,
        'tasks': tasks,
        'user': user
    }

    return render(request, 'taskrabbit/user_status.html', context)


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
def get_carriers(request):

    json_carriers = []

    try:
        carriers = Carrier.objects.all()
        for a_carrier in carriers:
            carrier_package = {
                'value': a_carrier.id,
                'text': a_carrier.name
            }
            json_carriers.append(carrier_package)

    except Carrier.DoesNotExist:
        pass

    return HttpResponse(json.dumps(json_carriers), content_type='application/json')


@login_required
def get_themes(request):

    json_themes = []

    try:
        themes = Theme.objects.all()
        for a_theme in themes:
            carrier_package = {
                'value': a_theme.id,
                'text': a_theme.name
            }
            json_themes.append(carrier_package)

    except Carrier.DoesNotExist:
        pass

    return HttpResponse(json.dumps(json_themes), content_type='application/json')


# update a task using x-editable
@login_required
def update_task_inline(request):
    name = request.POST['name']
    pk = request.POST['pk']
    value = request.POST['value']

    try:
        task = Task.objects.get(id=pk)

        if name == "owner":

            value_as_object = User.objects.get(id=value)

            if task.owner is not None:
                note_description = "Transferred from " + task.owner.first_name + " to " \
                               + value_as_object.first_name + " by " + request.user.first_name + "."
            else:
                note_description = "Assigned to " + value_as_object.first_name + " by " + request.user.first_name + "."

        elif name == "status":
            value_as_object = Status.objects.get(id=value)
            note_description = "Status changed to " + str(value_as_object).lower() + "."

        else:
            value_as_object = value
            note_description = None

        if note_description is not None:
            note_update = Note(task=task, user=request.user, status=task.status, content=note_description,
                               timestamp=datetime.now(), automatic_note=True)
            note_update.save()

        setattr(task, name, value_as_object)
        task.save()

    except Task.DoesNotExist:
        raise Http404

    return HttpResponse(status=200)


# update a task using a form
@login_required
def update_task_form(request):

    if 'task_id' in request.POST:
        try:
            task = Task.objects.get(id=request.POST['task_id'])
        except Task.DoesNotExist:
            raise Http404

        for data in request.POST:
            if data not in ['csrfmiddlewaretoken', 'task_id']:
                setattr(task, data, request.POST[data])

        task.save()

        return HttpResponseRedirect(reverse('taskrabbit:view_task', kwargs={'task_id': request.POST['task_id']}))
    else:
        raise Http404

@login_required
def add_note(request):
    task_id = request.POST['task_id']
    content = request.POST['content']

    task = Task.objects.get(id=task_id)

    new_note = Note(task=task, user=request.user, status=task.status, content=content, timestamp=datetime.now())

    new_note.save()

    task.last_worked_on = datetime.now()

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
        # 'hide_statuses': Status.objects.filter(show_in_table=False)
    }

    try:
        tasks = Task.objects.filter(status__show_in_table=True)
        context['tasks'] = tasks
        context['events'] = format_tasks_as_events(tasks)

    except Task.DoesNotExist:
        context['errors'] = "No tasks found."

    add_context(context, request)

    return render(request, 'taskrabbit/all_tasks.html', context)


@login_required
def edit_task(request, task_id):
    if not task_id:
        raise Http404

    try:
        task = Task.objects.get(id=task_id)

    except Task.DoesNotExist:
        raise Http404

    context = {
        'task': task,
    }

    return render(request, 'taskrabbit/edit_task.html', context)


@login_required
def email_task_owner(request):
    if 'task_id' and 'content' in request.POST:
        task_id = request.POST['task_id']
        email_content = request.POST['content']

        try:
            task = Task.objects.get(id=task_id)
            email_url = local_settings.SITE_URL + reverse('taskrabbit:view_task', kwargs={'task_id': task.id})

            html_email = format("%s<br><br>-- %s<br><br><a href='%s' target='_blank'>View task on TaskRabbit</a>" %
                                (email_content, request.user.get_full_name(), email_url))

            plaintext_email = email_content + "\n\n--" + request.user.get_full_name() + "\n\n"\
                                            + "View task on TaskRabbit: " + email_url

            task.owner.email_user("New alert on TaskRabbit: " + task.name, plaintext_email, html_message=html_email)

            messages.success(request, "Email sent successfully.")
            return HttpResponseRedirect(reverse('taskrabbit:view_task', kwargs={'task_id': task.id}))

        except Task.DoesNotExist:
            raise Http404

    else:
        raise Http404


def send_text_to_owner(request):
    if 'task_id' and 'content' in request.POST:
        task_id = request.POST['task_id']
        email_content = request.POST['content']

        try:
            task = Task.objects.get(id=task_id)
            email_url = local_settings.SITE_URL + reverse('taskrabbit:view_task', kwargs={'task_id': task.id})

            email_body = format("%s: %s [%s]" % (request.user.first_name, email_content, email_url))

            try:
                send_text_message(task.owner, "taskrabbit", email_body)
                messages.success(request, "Text sent successfully.")
            except PhoneNumber.DoesNotExist:
                messages.error(request, "User does not have a phone number.")

            return HttpResponseRedirect(reverse('taskrabbit:view_task', kwargs={'task_id': task.id}))

        except Task.DoesNotExist:
            raise Http404

    else:
        raise Http404


def format_tasks_as_events(tasks):
    events = []

    for task in tasks:
        if task.end_date:
            events.append({
                'title': task.name.replace('"', '\\"'),
                'allDay': True,
                'start': task.start_date.isoformat(),
                'end': task.end_date.isoformat(),
                'id': task.id,
                'owner': task.owner.first_name if task.owner else '--'
            })
        else:
            events.append({
                'title': task.name.replace('"', '\\"'),
                'allDay': True,
                'start': task.start_date.isoformat(),
                'id': task.id,
                'owner': task.owner.first_name if task.owner else '--'
            })

    return json.dumps(events)


@login_required
def update_user_profile(request):
    if 'csrfmiddlewaretoken' not in request.POST:
        context = {

        }

        add_context(context, request)
        return render(request, 'taskrabbit/edit_profile.html', context)
    else:
        user = request.user

        name = request.POST['name']
        pk = request.POST['pk']
        value = request.POST['value']

        # Update user normally
        if name not in ('phone_number', 'carrier', 'theme'):
            setattr(user, name, value)
            user.save()

        # Otherwise check if theme

        elif name != 'theme':
            try:
                phone_number = user.phonenumber
            except PhoneNumber.DoesNotExist:
                phone_number = PhoneNumber(user=user)

            if name == "carrier":
                value = Carrier.objects.get(id=value)

            setattr(phone_number, name, value)
            phone_number.save()

        else:
            try:
                profile = user.userprofile
            except UserProfile.DoesNotExist:
                profile = UserProfile(user=user)

            setattr(profile, name, Theme.objects.get(id=value))
            profile.save()

            json_response = {
                'status': 'notify',
            }

            return HttpResponse(json.dumps(json_response), content_type='application/json')

        return HttpResponse(status=200)


@login_required
def update_user_password(request):
    if 'csrfmiddlewaretoken'  in request.POST:

        old_password = request.POST['old_password']
        password = request.POST['password']

        if request.user.check_password(old_password):
            user = request.user
            user.set_password(password)
            user.save()
            messages.success(request, "Password changed successfully.")

        else:
            messages.error(request, "Your old password was entered incorrectly, please try again.")

    context = {}
    add_context(context, request)
    return render(request, 'taskrabbit/change_password.html', context)


def create_account(request, creation_id):

    try:
        token = AccountCreationID.objects.get(uuid=creation_id)
        if token.expire_date > timezone.now():
            if 'csrfmiddlewaretoken' not in request.POST:
                context = {
                    'email_address': token.email_address,
                    'carriers': Carrier.objects.all()
                }
                return render(request, 'taskrabbit/create_account.html', context)
            else:
                username = request.POST['username']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                password = request.POST['password']
                set_phone = False
                set_carrier = False

                if request.POST['phone_number']:
                    phone_number = request.POST['phone_number']
                    if request.POST['carrier']:
                        carrier = request.POST['carrier']
                        set_carrier = True
                    set_phone = True

                try:
                    new_user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)

                    if set_phone:
                        phone = PhoneNumber(user=new_user, phone_number=phone_number)
                        if set_carrier:
                            phone.carrier = Carrier.objects.get(id=carrier)
                        phone.save()

                    messages.success(request, "Account created successfully. You may now log in.")

                    token.delete()

                    return HttpResponseRedirect(reverse('taskrabbit:index'))
                except IntegrityError:
                    context = {
                        'email_address': token.email_address,
                        'carriers': Carrier.objects.all()
                    }
                messages.error(request, "That username already exists, please try again.")
                return render(request, 'taskrabbit/create_account.html', context)
                
        else:
            raise Http404

    except AccountCreationID.DoesNotExist:
        raise Http404


def forgot_password(request, password_id=False):
    if request.user.is_authenticated():
        logout(request)

    # If there's no ID
    if not password_id:
        if 'username' and 'email' in request.POST:
            username = request.POST['username']
            email_address = request.POST['email']

            try:
                user = User.objects.get(username=username, email=email_address)
                reset_id = PasswordResetID(user=user)
                email_url = local_settings.SITE_URL + reverse('taskrabbit:forgot_password',
                                                              kwargs={'password_id': reset_id.uuid})
                reset_id.save()

                user.email_user("TaskRabbit Password Reset", "You requested a password reset on TaskRabbit."
                                                             "\nTo continue, click the link below "
                                                             "(which will expire in 24 hours)."
                                                             "\n\n" + email_url, local_settings.SERVER_EMAIL)

                messages.success(request, "Request send successfully. Please check your email.")

            except User.DoesNotExist:
                messages.error(request, "Your information did not match any accounts, please try again.")

        return render(request, 'taskrabbit/forgot.html')

    # If there's an ID
    else:
        try:
            password_request = PasswordResetID.objects.get(uuid=password_id)
            if not password_request.expire_date > timezone.now():
                raise Http404

        except PasswordResetID.DoesNotExist:
            raise Http404

        if 'password' and 'password_verify' in request.POST:
            password = request.POST['password']
            password_verify = request.POST['password_verify']

            if password == password_verify:
                password_request.user.set_password(password)
                password_request.user.save()

                password_request.delete()

                messages.success(request, "Password reset successfully. You may now log in.")
                return HttpResponseRedirect(reverse('taskrabbit:login'))
            else:
                messages.error(request, "Your passwords did not match.")
                return render(request, 'taskrabbit/forgot_reset_form.html')

        else:
            return render(request, 'taskrabbit/forgot_reset_form.html')


