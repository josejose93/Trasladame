from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bus, Destination, Driver, Passenger, Seat, Ticket
from .serializers import BusSerializer, DestinationSerializer, DriverSerializer, PassengerSerializer, TicketSerializer
import json

class PassengerViewSet(viewsets.ModelViewSet):
    """ Create CRUD Passenger """

    serializer_class = PassengerSerializer
    queryset = Passenger.objects.all()


class DriverViewSet(viewsets.ModelViewSet):
    """ Create CRUD Driver """

    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class BusViewSet(viewsets.ModelViewSet):
    """ Create CRUD Bus """

    serializer_class = BusSerializer
    queryset = Bus.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        for i in range(10):
            Seat.objects.create(
                number=i+1,
                bus= Bus.objects.get(license_plate=request.data['license_plate']),
                state=False
                )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DestinationViewSet(viewsets.ModelViewSet):
    """ Create CRUD Destination """

    serializer_class = DestinationSerializer
    queryset = Destination.objects.all()


class TicketViewSet(viewsets.ModelViewSet):
    """ Create CRUD Ticket """

    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        seat = Seat.objects.get(id=request.data['seat_id'])
        seat.state = True
        seat.save()
        bus = Destination.objects.get(id=request.data['destination_id'])
        bus.seat_taken = bus.seat_taken + 1
        bus.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DestinationAveragePassengerApiView(APIView):
    """ List the destination with the average of passengers """

    def get(self, request, format=None):
        destinations_distinct = Destination.objects.distinct('departure_place', 'arrival_place')

        data = []
        destination = {}

        for d in destinations_distinct:
            destination_all = Destination.objects.filter(
                departure_place__iexact=d.departure_place,
                arrival_place__iexact=d.arrival_place
                )
            destination['destination'] = d.departure_place + '-' + d.arrival_place
            number_passenger = []
            for i in destination_all:
                number_passenger.append(i.seat_taken)
            

            destination['passenger_average'] = sum(number_passenger) / len(destination_all)
            data.append(destination)
            destination = {}

        data_json = json.dumps(data)
        return Response({'results': json.loads(data_json)})


class BusesOverflowApiView(APIView):
    """ List of buses with overflow passengers """

    def get(self, request, format=None):
        queryset = Destination.objects.filter(seat_taken__gt=10)
        buses = []

        for d in queryset:
            buses.append(d.bus)

        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
