from django.urls import path, include
from rest_framework.routers import DefaultRouter
from busAgency import views
 
app_name = 'busAgency'

router = DefaultRouter()
router.register('passenger', views.PassengerViewSet)
router.register('driver', views.DriverViewSet)
router.register('bus', views.BusViewSet)
router.register('destination', views.DestinationViewSet)
router.register('ticket', views.TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]