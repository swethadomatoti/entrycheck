from django.db import models

class Visitor(models.Model):
     PURPOSE_CHOICES = [
        ('Business Meeting', 'Business Meeting'),
        ('Interview', 'Interview'),
        ('Delivery', 'Delivery'),
        ('Maintenance', 'Maintenance'),
        ('Personal Visit', 'Personal Visit'),
        ('Other', 'Other'),
    ]
     full_name = models.CharField(max_length=100)
     email = models.EmailField(max_length=100)
     phone_number = models.CharField(max_length=15)
     purpose = models.CharField(max_length=200, choices=PURPOSE_CHOICES)
     host = models.CharField(max_length=100)                
     additional_details = models.TextField(blank=True, null=True)
     entry_time = models.DateTimeField(auto_now_add=True)  

     def __str__(self):
        return f"{self.full_name} visiting {self.host}"
