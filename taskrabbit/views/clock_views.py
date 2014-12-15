from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from datetime import datetime

import json

from taskrabbit.models import TimeLog, NfcCard

from taskrabbit.utils.time_utils import get_total_time, strfdelta


ENTRIES_PER_PAGE = 5
TIME_LOG_EXPIRATION_HOURS = 18
RESET_MONTH = 5  # May
RESET_DAY = 1

# Create your views here.



@login_required
def auth_home_view(request, page):

    user = request.user

    page = int(float(page))

    try:
        # Look up their time logs
        raw_time_logs = TimeLog.objects.filter(user=user, valid=True)

        time_log_size = len(TimeLog.objects.filter(user=user, valid=True))

        begin_entries = 0
        end_entries = ENTRIES_PER_PAGE

        begin_entries += (page - 1) * ENTRIES_PER_PAGE
        end_entries += (page - 1) * ENTRIES_PER_PAGE

        # if the page is larger than all the entries, it's not
        if end_entries > time_log_size:
            end_entries = time_log_size

        last_ten = TimeLog.objects.filter(user=user, valid=True).order_by('-id')[begin_entries:end_entries]

        time_logs = []

        for aTime in last_ten:

            # Check if they've gone out yet
            if aTime.exit_time:
                exit_time_checked = aTime.exit_time.time()
                total_time_checked = strfdelta((aTime.exit_time - aTime.entry_time), "{H}h {M}m")
            else:
                exit_time_checked = "Not yet clocked out."
                total_time_checked = "n/a"

            time_logs.append({
                "valid": aTime.valid,
                "date":  aTime.entry_time.date(),
                "entry_time": aTime.entry_time.time(),
                "exit_time": exit_time_checked,
                "total_time": total_time_checked,
            })

        # Look up their latest time log
        latest_log = raw_time_logs.latest('id')
        if not latest_log.exit_time:
            currently_timed_in = True
        else:
            currently_timed_in = False

        context = {
            'time_logs': time_logs,

            # Subtract total from the same original time to get the difference
            'grand_total_time': strfdelta(get_total_time(raw_time_logs), "{H}h {M}m"),
            'currently_timed_in': currently_timed_in,
            'next_page': page + 1,
            'back_page': page - 1,
            'first_page': page == 1,
            'last_page': end_entries == time_log_size,

            # begin_entries has 1 added to it, because order_by()[:] is [inclusive:exclusive] and 0-based
            'begin_entries': begin_entries + 1,
            'end_entries': end_entries
        }
    except TimeLog.DoesNotExist:
        context = {}

    # Pass all context variables and load the page
    context['user'] = user

    return render(request, 'robomanage/auth_home.html', context)

def index_view(request, page=1):
    if request.user.is_authenticated():
        return HttpResponse(auth_home_view(request, page))

    # Otherwise, redirect to login page
    else:
        context = {
           'login_form': LoginForm
        }

        return render(request, 'robomanage/index.html', context)


def login_view(request):
    if request.POST.get("username") and request.POST.get("password"):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        return login_helper(request, user)

    else:
        return HttpResponseRedirect(reverse('taskrabbit:index'))


# @csrf_exempt
# # def login_with_nfc_view(request):
# #     if request.POST['serial_number'] and request.POST['secret_key']:
# #         try:
# #             valid_card = NfcCard.objects.get(serial_number=request.POST['serial_number'], secret_key=request.POST['secret_key'])
# #             user = authenticate(username=valid_card.user.username, no_password=True)
# #             # return HttpResponse(user.get_full_name())
# #             return login_helper(request, user, True)
# #         except NfcCard.DoesNotExist:
# #             return HttpResponse("Invalid card.")
# #     else:
# #         return HttpResponse("Invalid request!")


# Performs generic log in methods for either NFC or normal log in
def login_helper(request, user, using_nfc=False):
    if user is not None:
        if user.is_active:

            # Check if they have any open TimeLog entries more than x hours - if so, cancel them
            time_logs = TimeLog.objects.filter(user=user, valid=True, exit_time=None)

            for log in time_logs:
                if((timezone.now() - log.entry_time).seconds * 3600) > TIME_LOG_EXPIRATION_HOURS:
                    log.valid = False

            login(request, user)
            if using_nfc:
                return HttpResponse("200 Success")
            else:
                return HttpResponseRedirect(reverse('taskrabbit:index'))
        else:
            if using_nfc:
               return HttpResponse("Your user account has been deactivated. Please contact an administrator.")
            else:
                messages.error(request, "Your user account has been deactivated. Please contact an administrator.")
                return HttpResponseRedirect(reverse('taskrabbit:index'))
    else:
        if using_nfc:
            return HttpResponse("Your tag is invalid.")
        else:
            messages.error(request, "Your username or password are incorrect.")
            return HttpResponseRedirect(reverse('taskrabbit:index'))


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return HttpResponseRedirect(reverse('taskrabbit:index'))


@login_required
def clock_in_view(request):

    # Get the user
    user = request.user

    # Look up their time logs
    try:
        latest_log = TimeLog.objects.filter(user=user).latest('id')
        if latest_log.exit_time:
            a_time = TimeLog(user=user, entry_time=timezone.now())
            a_time.save()
            # messages.success(request, "Clocked in successfully.")
            return HttpResponseRedirect(reverse('taskrabbit:index'))
        else:
            messages.error(request, "You must clock out first.")
            return HttpResponseRedirect(reverse('taskrabbit:index'))
    except TimeLog.DoesNotExist:
            a_time = TimeLog(user=user, entry_time=timezone.now())
            a_time.save()
            # messages.success(request, "Clocked in successfully.")
            return HttpResponseRedirect(reverse('taskrabbit:index'))


@login_required
def clock_out_view(request):

    user = request.user

     # Look up their time logs
    latest_log = TimeLog.objects.filter(user=user).latest('id')
    if not latest_log.exit_time:
        latest_log.exit_time = timezone.now()
        latest_log.save()
        # messages.success(request, "Clocked out successfully.")
        print(request.path)
        if '/times' in request.path:
            return HttpResponseRedirect(reverse('taskrabbit:time_history'))
        else:
            return HttpResponseRedirect(reverse('taskrabbit:index'))
    else:
        messages.error(request, "You must clock in first.")
        return HttpResponseRedirect(reverse('taskrabbit:index'))

@login_required
def time_history(request):

    user = request.user

    # Look up their time logs
    time_logs = TimeLog.objects.filter(user=user, valid=True)

    current_time_length = 0
    grand_total_time = 0
    if len(time_logs) > 0:
        if not time_logs.latest('id').exit_time:
            currently_timed_in = True
            current_time_length = int((timezone.now() -
                        time_logs.latest('id').entry_time).total_seconds())
            time_logs = time_logs.exclude(exit_time=None)
        else:
            currently_timed_in = False
        grand_total_time = int(get_total_time(time_logs).total_seconds())
        if currently_timed_in:
            grand_total_time += current_time_length
    else:
        currently_timed_in = False

    logs = []
    for log in time_logs:
        delta = log.exit_time - log.entry_time
        logs.append({
            'entry_time': log.entry_time,
            'exit_time': log.exit_time,
            'time_length': strfdelta(delta, "{HH}:{MM}")
        })

    context = {
        'logs': logs,
        'currently_timed_in': currently_timed_in,
        'current_time_length': current_time_length,
        'total_time': grand_total_time
    }

    return render(request, 'taskrabbit/time_history.html', context)


# Views for working with NFC cards - these do not require sessions,
# but auth the user by their card every time they are called

# Check if a user is currently clocked in
@csrf_exempt
def check_if_clocked_in(request):
    if request.POST['serial_number'] and request.POST['secret_key']:
        try:
            valid_card = NfcCard.objects.get(serial_number=request.POST['serial_number'], secret_key=request.POST['secret_key'])
            user = authenticate(username=valid_card.user.username, no_password=True)
        except NfcCard.DoesNotExist:
            return HttpResponse("Invalid NFC card.")
        if user is not None:
            if user.is_active:
                latest_log = TimeLog.objects.filter(user=user).latest('id')
                if latest_log.exit_time:
                    return HttpResponse(False)
                else:
                    return HttpResponse(True)
            else:
                return HttpResponse("Invalid user account (inactive).")
        else:
            return HttpResponse("Invalid user account (does not exist).")
    else:
        return HttpResponse("Invalid request.")


# Clock out if in, or in if out
@csrf_exempt
def toggle_clocked_in(request):
    if request.POST['serial_number'] and request.POST['secret_key']:
        try:
            valid_card = NfcCard.objects.get(serial_number=request.POST['serial_number'], secret_key=request.POST['secret_key'])
            user = authenticate(username=valid_card.user.username, no_password=True)
        except NfcCard.DoesNotExist:
            return HttpResponse("Invalid NFC card.")
        if user is not None:
            if user.is_active:
                # Look up their time logs
                try:
                    latest_log = TimeLog.objects.filter(user=user).latest('id')
                    if latest_log.exit_time:
                        a_time = TimeLog(user=user, entry_time=timezone.now())
                        a_time.save()
                        return HttpResponse("in")
                    else:
                        latest_log.exit_time = timezone.now()
                        latest_log.save()
                        return HttpResponse("out")
                except TimeLog.DoesNotExist:
                        a_time = TimeLog(user=user, entry_time=timezone.now())
                        a_time.save()
                        return HttpResponse("in")
            else:
                return HttpResponse("Invalid user account (inactive).")
        else:
            return HttpResponse("Invalid user account (does not exist).")
    else:
        return HttpResponse("Invalid request.")


def supervisor_view(request):
    return render(request, 'robomanage/supervisor_panel.html')


def history_view(request, username=None):
    if username is not None and username is not request.user.username and not request.user.is_superuser:
        return HttpResponse("Unauthorized")

    if username is not None:
        this_user = User.objects.get(username=username)
    else:
        this_user = request.user

    try:
        logs_for_user = TimeLog.objects.filter(user=this_user, valid=True)
        json_list = []

        for a_log in logs_for_user:
            id = "foo"
            title = strfdelta(a_log.exit_time - a_log.entry_time, "{H}h {M}m")
            start = a_log.entry_time.strftime("%Y-%m-%dT%H:%M:%S")
            end = a_log.exit_time.strftime("%Y-%m-%dT%H:%M:%S")
            allDay = False

            json_entry = {
                'id': id,
                'title': title,
                'start': start,
                'end': end,
                'allDay': allDay
            }

            json_list.append(json_entry)

    except TimeLog.DoesNotExist:
        logs_for_user = None



    context = {
        'calendar_logs': json.dumps(json_list, ensure_ascii=False),
        'user': this_user
    }

    return render(request, 'robomanage/history.html', context)


def supervisor_clock_all_out(request):
    try:
        open_logs = TimeLog.objects.filter(exit_time=None)
        for a_log in open_logs:
            a_log.exit_time = timezone.now()
            a_log.save()
        if len(open_logs) == 1:
            messages.success(request, "Clocked 1 person out.")
        else:
            messages.success(request, "Clocked " + str(len(open_logs)) + " people out.")

    except TimeLog.DoesNotExist:
        messages.error(request, "Nobody to clock out.")

    return HttpResponseRedirect(reverse('robomanage:supervisor_view'))


def supervisor_all_users_view(request):
    all_active_users = User.objects.filter(is_active=True).order_by('first_name')

    all_user_data = []

    for a_user in all_active_users:
        their_time_logs = TimeLog.objects.filter(user=a_user, valid=True)
        total_time = strfdelta(get_total_time(their_time_logs), "{H}h {M}m")

        all_user_data.append([
            a_user,
            total_time
        ])

    context = {
        'all_user_data': all_user_data
    }

    return render(request, 'robomanage/supervisor_all_users.html', context)
