from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.utils import timezone


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
    workflow = models.ForeignKey(WorkFlow, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.workflow} - Step {self.step_number}"


class HistoryTrackingMixin(models.Model):
    """Mixin for automatically tracking history of model changes.

    This mixin provides functionality to automatically track the history
    of changes made to instances of a Django model. It creates historical
    records in a separate history table whenever a model instance is updated.

    Methods:
    - save_history: Creates a historical record for the current state of the model.
    - save: Overrides the default save method to save the historical record
            after updating the model instance.

    Usage:
    - Inherit from this mixin in your Django model class to enable history tracking.
    """

    def save_history(self):
        historical_data = {field.name: getattr(
            self, field.name) for field in self._meta.fields}
        historical_data['timestamp'] = timezone.now()
        history_model = self.__class__.__name__ + 'History'
        history_instance = globals()[history_model].objects.create(
            **historical_data)
        return history_instance

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)

        if not creating:
            self.save_history()

    class Meta:
        abstract = True


class Requests(HistoryTrackingMixin, models.Model):

    REQUEST_STATUS_PENDING = 'pending'
    REQUEST_STATUS_NEXT = 'next'
    REQUEST_STATUS_REJECT = 'reject'
    REQUEST_STATUS_ROLLBACK = 'rollback'
    REQUEST_STATUS_ACCEPT = 'accept'

    REQUEST_STATUS = [
        (REQUEST_STATUS_PENDING, 'Pending'),
        (REQUEST_STATUS_NEXT, 'Next'),
        (REQUEST_STATUS_REJECT, 'Reject'),
        (REQUEST_STATUS_ROLLBACK, 'Rollback'),
        (REQUEST_STATUS_ACCEPT, 'Accept')
    ]

    name = models.CharField(max_length=255)
    desc = models.TextField()
    workflow = models.ForeignKey(WorkFlow, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    status = models.CharField(choices=REQUEST_STATUS,
                              default=REQUEST_STATUS_PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RequestsHistory(models.Model):
    REQUEST_STATUS_PENDING = 'pending'
    REQUEST_STATUS_NEXT = 'next'
    REQUEST_STATUS_REJECT = 'reject'
    REQUEST_STATUS_ROLLBACK = 'rollback'
    REQUEST_STATUS_ACCEPT = 'accept'

    REQUEST_STATUS = [
        (REQUEST_STATUS_PENDING, 'Pending'),
        (REQUEST_STATUS_NEXT, 'Next'),
        (REQUEST_STATUS_REJECT, 'Reject'),
        (REQUEST_STATUS_ROLLBACK, 'Rollback'),
        (REQUEST_STATUS_ACCEPT, 'Accept')
    ]

    name = models.CharField(max_length=255)
    desc = models.TextField()
    workflow = models.ForeignKey(WorkFlow, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    status = models.CharField(choices=REQUEST_STATUS,
                              default=REQUEST_STATUS_PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-timestamp']
