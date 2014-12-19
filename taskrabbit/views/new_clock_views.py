from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

import json

from taskrabbit.models import TimeLog, NfcCard

from taskrabbit.utils.time_utils import get_total_time, strfdelta

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
        return HttpResponseRedirect(reverse('taskrabbit:index'))
    else:
        messages.error(request, "You must clock in first.")
        return HttpResponseRedirect(reverse('taskrabbit:index'))
