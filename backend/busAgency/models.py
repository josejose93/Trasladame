from django.db import models

class UserBus(models.Model):
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    dni = models.CharField(max_length=8, null=False, unique=True)

    class Meta:
        abstract = True


class Passenger(UserBus):
    pass


class Driver(UserBus):
    is_working =models.BooleanField(default=False, null=False) 


class Bus(models.Model):
    license_plate = models.CharField(max_length=10, null=False, unique=True)
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)


class Seat(models.Model):
    number = models.IntegerField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    state = models.BooleanField(default=False, null=False)


class Destination(models.Model):
    departure_place = models.CharField(max_length=20, null=False)
    arrival_place = models.CharField(max_length=20, null=False)
    duration = models.TimeField()
    schedule = models.DateTimeField(auto_now=False, auto_now_add=False, null=False)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_taken = models.IntegerField(default=0, null=False)

    class Meta:
        unique_together = [['schedule', 'bus']]


class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['passenger', 'creation_date']]
        ordering = ('creation_date',)
