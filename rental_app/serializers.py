from rest_framework import serializers
from .models import Property, Room, Tenant, Occupation, Contract, Bill

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    property_details = PropertySerializer(source='property', read_only=True)
    
    class Meta:
        model = Room
        fields = ('property', 'property_details', 'price', 'status', 'size')

class TenantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='tenant.name', read_only=True)
    phone = serializers.CharField(source='tenant.phone', read_only=True)
    dni = serializers.CharField(source='tenant.DNI', read_only=True)
    
    class Meta:
        model = Tenant
        fields = ('name', 'phone', 'dni', 'reason_leave')

class OccupationSerializer(serializers.ModelSerializer):
    tenant_details = TenantSerializer(source='tenant', read_only=True)
    room_details = RoomSerializer(source='room', read_only=True)
    
    class Meta:
        model = Occupation
        fields = ('tenant', 'tenant_details', 'room', 'room_details', 'check_in', 'check_out')

class ContractSerializer(serializers.ModelSerializer):
    property_details = PropertySerializer(source='property', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    
    class Meta:
        model = Contract
        fields = ('user_name', 'property', 'property_details')

class BillSerializer(serializers.ModelSerializer):
    property_details = PropertySerializer(source='property', read_only=True)
    
    class Meta:
        model = Bill
        fields = ('utility', 'property', 'property_details', 'type')
