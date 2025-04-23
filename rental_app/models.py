from django.db import models
from users.models import ProfileUser

REGION_CHOICES = [
    ('I', 'Tarapacá'),
    ('II', 'Antofagasta'),
    ('III', 'Atacama'),
    ('IV', 'Coquimbo'),
    ('V', 'Valparaíso'),
    ('RM', 'Región Metropolitana'),
    ('VI', 'Libertador General Bernardo O’Higgins'),
    ('VII', 'Maule'),
    ('VIII', 'Biobío'),
    ('IX', 'La Araucanía'),
    ('X', 'Los Lagos'),
    ('XI', 'Aysén del General Carlos Ibáñez del Campo'),
    ('XII', 'Magallanes y de la Antártica Chilena'),
    ('XIV', 'Los Ríos'),
    ('XV', 'Arica y Parinacota'),
    ('XVI', 'Ñuble'),
]

TYPE_CHOICES = [
    ('House', 'House'),
    ('Apartment', 'Apartment'),
    ('Studio', 'Studio')
]

STATUS_CHOICES = [
    ('A', 'Available'),
    ('O', 'Occupied'),
    ('M', 'Maintenance'),
]

SIZE_CHOICES = [
    ('Small', 'Small'),
    ('Medium', 'Medium'),
    ('Large', 'Large'),
]

BILL_CHOICES = [
    ('Electricity', 'Electricity'),
    ('Water', 'Water'),
    ('Internet', 'Internet'),
    ('Gas', 'Gas'),
    ('Maintenance', 'Maintenance'),
    ('Other', 'Other'),
]

class Property(models.Model):
    region = models.CharField(max_length=30, choices=REGION_CHOICES, blank=True, null=True)
    direction = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(default="default.png", blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    qty_bathrooms = models.SmallIntegerField(blank=True, null=True, default=0)
    qty_rooms = models.SmallIntegerField(blank=True, null=True, default=0)
    area = models.IntegerField(default=0, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"{self.direction} ({self.region})"

class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, null=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return f"Room {self.property.direction}"

class Tenant(models.Model):
    tenant = models.OneToOneField(ProfileUser, on_delete=models.CASCADE, related_name='tenant_profile')
    reason_leave = models.TextField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"Tenant: {self.tenant.name}"

class Occupation(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='occupations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='occupations')
    check_in = models.DateTimeField(blank=True, null=True)
    check_out = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('tenant', 'room', 'check_in')
    
    def __str__(self):
        return f"{self.tenant.tenant.name} in {self.room} from {self.check_in}"

class Contract(models.Model):
    user = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='contract')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='contracts')
    
    def __str__(self):
        return f"Contract: {self.user.name} - {self.property.direction}"

class Bill(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bills')
    utility = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type = models.CharField(max_length=50, choices=BILL_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return f"Bill for {self.property.direction} ({self.type})"

