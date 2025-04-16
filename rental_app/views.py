from django.db.models import Sum, Count, Avg, F, Q
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Property, Room, Tenant, Occupation, Contract, Bill
from .serializers import (
    PropertySerializer, 
    RoomSerializer, 
    TenantSerializer, 
    OccupationSerializer,
    ContractSerializer,
    BillSerializer
)

class IsOwnerOrReadOnly(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user has a contract for this property
        try:
            return Contract.objects.filter(user__user=request.user, property=obj).exists()
        except:
            return False

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        
        total_properties = Property.objects.count()
        occupied_rooms = Room.objects.filter(status='O').count()
        total_rooms = Room.objects.count()
        occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
        
        # Calculate average price by region
        avg_price_by_region = Property.objects.values('region').annotate(
            avg_price=Avg('price')
        ).order_by('region')
        
        # Calculate total earnings
        total_earnings = Occupation.objects.filter(
            check_out__isnull=False
        ).aggregate(
            total=Sum(F('room__price'))
        )['total'] or 0
        
        return Response({
            'total_properties': total_properties,
            'total_rooms': total_rooms,
            'occupied_rooms': occupied_rooms,
            'occupancy_rate': occupancy_rate,
            'avg_price_by_region': avg_price_by_region,
            'total_earnings': total_earnings
        })
    
    @action(detail=False, methods=['get'])
    def region_stats(self, request):
      
        regions = Property.objects.values('region').annotate(
            count=Count('id'),
            avg_price=Avg('price'),
            total_rooms=Sum('rooms'),
            occupancy=Count('rooms__occupations', filter=Q(rooms__status='O'))
        ).order_by('-count')
        
        return Response(regions)

class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
       
        room = self.get_object()
        total_occupations = Occupation.objects.filter(room=room).count()
        current_occupation = Occupation.objects.filter(
            room=room, 
            check_in__isnull=False,
            check_out__isnull=True
        ).first()
        
        # Get occupation history
        occupation_history = Occupation.objects.filter(
            room=room
        ).order_by('-check_in')
        
        return Response({
            'room_id': room.id,
            'property': room.property.direction,
            'total_occupations': total_occupations,
            'is_currently_occupied': current_occupation is not None,
            'current_tenant': current_occupation.tenant.tenant.name if current_occupation else None,
            'occupation_history': OccupationSerializer(occupation_history, many=True).data
        })

class TenantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
       
        tenant = self.get_object()
        occupations = Occupation.objects.filter(tenant=tenant).order_by('-check_in')
        
        return Response(OccupationSerializer(occupations, many=True).data)

class OccupationViewSet(viewsets.ModelViewSet):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer
    permission_classes = [permissions.IsAuthenticated]

class EarningsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
       
        # Calculate total earnings from all occupations
        total_earnings = Occupation.objects.filter(
            check_out__isnull=False
        ).aggregate(
            total=Sum(F('room__price'))
        )['total'] or 0
        
        return Response({
            'total_earnings': total_earnings
        })

class EarningsByRegionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
      
        earnings_by_region = Property.objects.values('region').annotate(
            total_earnings=Sum(
                F('rooms__occupations__room__price'),
                filter=Q(rooms__occupations__check_out__isnull=False)
            )
        ).order_by('-total_earnings')
        
        return Response(earnings_by_region)

class EarningsByOwnerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
       
        owner_id = request.query_params.get('owner_id')
        if not owner_id:
            return Response(
                {"error": "owner_id parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        earnings = Contract.objects.filter(
            user_id=owner_id
        ).values(
            'property__region'
        ).annotate(
            total_earnings=Sum(
                F('property__rooms__occupations__room__price'),
                filter=Q(property__rooms__occupations__check_out__isnull=False)
            )
        ).order_by('-total_earnings')
        
        return Response(earnings)

