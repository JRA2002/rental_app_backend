from django.contrib import admin
from .models import Property, Room, Tenant, Occupation, Contract, Bill
# Register your models here.

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('region', 'direction', 'type', 'price', 'status', 'qty_bathrooms', 'qty_rooms', 'area')
    search_fields = ('direction', 'region')
    list_filter = ('status', 'type')
    ordering = ('price',)
    list_per_page = 10

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('property', 'price', 'status', 'size')
    search_fields = ('property__direction',)
    list_filter = ('status',)
    ordering = ('price',)
    list_per_page = 10

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'reason_leave')
    search_fields = ('tenant__name',)
    list_filter = ('reason_leave',)
    ordering = ('tenant__name',)
    list_per_page = 10


@admin.register(Occupation)
class OccupationAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'room', 'check_in', 'check_out')
    search_fields = ('tenant__tenant__name', 'room__property__direction')
    list_filter = ('check_in', 'check_out')
    ordering = ('check_in',)
    list_per_page = 10

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('user', 'property')
    search_fields = ('user__name', 'property__direction')
    list_filter = ('property__type',)
    ordering = ('user__name',)
    list_per_page = 10

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('utility', 'property', 'type')
    search_fields = ('property__direction',)
    list_filter = ('type',)
    ordering = ('utility',)
    list_per_page = 10
    
