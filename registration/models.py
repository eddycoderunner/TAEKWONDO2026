from django.db import models
import uuid

class Registration(models.Model):
    registration_number = models.CharField(max_length=20, unique=True, blank=True, null=True) 
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    club_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    weight_category = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            self.registration_number = f"TKD-2026-{self.id:03d}"
            Registration.objects.filter(id=self.id).update(
                registration_number=self.registration_number
            )


    def __str__(self):
        return self.full_name
