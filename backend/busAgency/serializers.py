from dataclasses import field
from rest_framework import serializers
from .models import Destination, Passenger, Driver, Bus, Seat, Ticket

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
  driver_id = serializers.IntegerField(write_only=True)

  class Meta:
    model = Bus
    fields = ('id', 'license_plate', 'driver', 'driver_id', 'seat_taken')
    depth = 1


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields = '__all__'


class DestinationSerializer(serializers.ModelSerializer):
    bus_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Destination
        fields = ('id', 'departure_place', 'arrival_place', 'duration', 'schedule', 'bus', 'bus_id')
        depth = 2


class TicketSerializer(serializers.ModelSerializer):
    passenger_id = serializers.IntegerField(write_only=True)
    destination_id = serializers.IntegerField(write_only=True)
    seat_id = serializers.IntegerField(write_only=True)
    creation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=["%Y-%m-%d %H:%M:%S"])
    
    class Meta:
        model = Ticket
        fields = ('id', 'passenger', 'passenger_id',  'destination', 'destination_id', 'seat', 'seat_id', 'creation_date')
        depth = 2
