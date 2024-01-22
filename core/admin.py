from django.contrib import admin
from .models import WorkFlow, Step, Requests, RequestsHistory
# Register your models here.

admin.site.register(WorkFlow)
admin.site.register(Step)
admin.site.register(Requests)
admin.site.register(RequestsHistory)
