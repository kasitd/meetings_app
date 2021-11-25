from  datetime import time
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Room(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField()
    floor = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return f'Sala: {self.name}, nr: {self.number}, piętro: {self.floor}'


class MeetingQuerySet(models.QuerySet):
    def meetings_for_user(self, user):
        return self.filter(
            Q(author=user) | Q(participants=user)
        ).distinct()



class Meeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField(default=time(9))
    end_time = models.TimeField(default=time(17))
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=User)
    participants = models.ManyToManyField(User, related_name='participants', null=True, blank=True)

    objects = MeetingQuerySet.as_manager()

    def __str__(self):
        return f"Spotkanie: {self.title} o godzinie: {self.start_time}"
