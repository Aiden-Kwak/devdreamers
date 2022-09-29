from django.db import models

# Create your models here.
from accountapp.models import User
from contestapp.models import Contest
from teamapp.models import Team


class TeamSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribe')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='subscribe')

    class Meta:
        unique_together = ('user', 'team')

class ContestSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribe_contest')
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='subscribe_contest')

    class Meta:
        unique_together = ('user', 'contest')