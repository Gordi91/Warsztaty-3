from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=120, verbose_name='Nazwa')
    capacity = models.PositiveSmallIntegerField(verbose_name='Pojemność sali')
    is_projector_available = models.BooleanField(verbose_name='Dostępność rzutnika', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Sale'


class Reservation(models.Model):
    date = models.DateField(verbose_name='Data rezerwacji')
    room = models.ForeignKey(Room, verbose_name='Sala', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Komentarz')

    def __str__(self):
        return f'ID: {self.id}, Data rezerwacji: {self.date}'

    class Meta:
        verbose_name = 'Rezerwacja'
        verbose_name_plural = 'Rezerwacje'
        unique_together = ("date", "room")
