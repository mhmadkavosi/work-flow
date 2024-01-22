from django.db import models
from django.contrib.auth.models import User


class Leave(models.Model):
    REQUEST_STATUS_PENDING = 'pending'
    REQUEST_STATUS_ACCEPT = 'accept'
    REQUEST_STATUS_REJECT = 'reject'

    REQUEST_STATUS = [
        (REQUEST_STATUS_PENDING, 'Pending'),
        (REQUEST_STATUS_ACCEPT, 'Accept'),
        (REQUEST_STATUS_REJECT, 'Reject')
    ]

    reason = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=REQUEST_STATUS,
                              default=REQUEST_STATUS_PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reason} - {self.user} - {self.status}"
