from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone


class WorkFlowModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StepModel(models.Model):
    name = models.CharField(max_length=255)
    user_owner = models.CharField(max_length=255)
    step_number = models.PositiveIntegerField(default=0)
    work_flow = models.ForeignKey(WorkFlowModel, on_delete=models.CASCADE),
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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


class RequestModel(HistoryTrackingMixin, models.Model):

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
    work_flow = models.ForeignKey(WorkFlowModel, on_delete=models.CASCADE)
    step = models.ForeignKey(StepModel, on_delete=models.CASCADE)
    status = models.CharField(choices=REQUEST_STATUS,
                              default=REQUEST_STATUS_PENDING)
    user = models.CharField(max_length=255)
    reason = models.CharField(max_length=255, null=True)
    request_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RequestHistoryModel(models.Model):
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
    work_flow = models.ForeignKey(WorkFlowModel, on_delete=models.CASCADE)
    step = models.ForeignKey(StepModel, on_delete=models.CASCADE)
    status = models.CharField(choices=REQUEST_STATUS,
                              default=REQUEST_STATUS_PENDING)
    user = models.CharField(max_length=255)
    reason = models.CharField(max_length=255, null=True)
    request_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
