from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Bus, Destination, Driver, Passenger, Seat, Ticket
from .serializers import BusSerializer, DestinationSerializer, DriverSerializer, PassengerSerializer, TicketSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    """ Create CRUD Passenger """

    serializer_class = PassengerSerializer
    queryset = Passenger.objects.all()


class DriverViewSet(viewsets.ModelViewSet):
    """ Create CRUD Driver """

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class BusViewSet(viewsets.ModelViewSet):
    """ Create CRUD Bus """

    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    
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
