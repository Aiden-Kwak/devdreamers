from django.db import models
from django.utils import timezone

import accountapp


class LandingChat(models.Model):
    writer = models.ForeignKey('accountapp.User', on_delete=models.CASCADE, related_name='landing_chat', null=True)
    date = models.DateTimeField(default=timezone.now)
    chat = models.TextField(blank=False, null=True, max_length=300)
