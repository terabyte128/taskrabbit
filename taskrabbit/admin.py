from django.contrib import admin

# Register your models here.
from taskrabbit.models import Task, Note, Team, UserProfile, Status, TimeLog

admin.site.register(Task)
admin.site.register(Note)
admin.site.register(Team)
admin.site.register(UserProfile)
admin.site.register(Status)
admin.site.register(TimeLog)
