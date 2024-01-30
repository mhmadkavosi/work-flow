from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from vacation.models import Leave


class WorkFlow(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Step(models.Model):
    name = models.CharField(max_length=255)
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField(default=0)
    workflow = models.ForeignKey(
        WorkFlow, on_delete=models.CASCADE, related_name='step_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.workflow} - Step {self.step_number}"


class RequestsHistory(models.Model):
    REQUEST_STATUS_PENDING = 'pending'
    REQUEST_STATUS_NEXT = 'next'
    REQUEST_STATUS_REJECT = 'reject'
    REQUEST_STATUS_ACCEPT = 'accept'

    REQUEST_STATUS = [
        (REQUEST_STATUS_PENDING, 'Pending'),
        (REQUEST_STATUS_NEXT, 'Next'),
        (REQUEST_STATUS_REJECT, 'Reject'),
        (REQUEST_STATUS_ACCEPT, 'Accept')
    ]
    request_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    desc = models.TextField()
    workflow = models.ForeignKey(WorkFlow, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    status = models.CharField(choices=REQUEST_STATUS,
                              default=REQUEST_STATUS_PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, null=True)
    leave = models.ForeignKey(Leave, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-timestamp']


class Requests(models.Model):

    REQUEST_STATUS_PENDING = 'pending'
    REQUEST_STATUS_NEXT = 'next'
    REQUEST_STATUS_REJECT = 'reject'
    REQUEST_STATUS_ACCEPT = 'accept'

    REQUEST_STATUS = [
        (REQUEST_STATUS_PENDING, 'Pending'),
        (REQUEST_STATUS_NEXT, 'Next'),
        (REQUEST_STATUS_REJECT, 'Reject'),
        (REQUEST_STATUS_ACCEPT, 'Accept')
    ]

    name = models.CharField(max_length=255)
    desc = models.TextField()
    workflow = models.ForeignKey(
        WorkFlow, on_delete=models.CASCADE)
    step = models.ForeignKey(
        Step, on_delete=models.CASCADE)
    status = models.CharField(choices=REQUEST_STATUS,
                              default=REQUEST_STATUS_PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, null=True)
    leave = models.ForeignKey(
        Leave, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save_history(self):
        RequestsHistory.objects.create(name=self.name, desc=self.desc, workflow=self.workflow,
                                       step=self.step, status=self.status, user=self.user, reason=self.reason,
                                       leave=self.leave, request_id=self.id)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_history()
