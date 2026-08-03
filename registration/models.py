from django.db import models
import random
import string

class Registration(models.Model):
    registration_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    club_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    weight_category = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def generate_registration_number(self):
        while True:

            chars = string.ascii_uppercase + string.digits
            random_part = ''.join(random.choices(chars, k=5))
            reg_number = f"TKD-{random_part}"

            if not Registration.objects.filter(registration_number=reg_number).exists():
                return reg_number

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new and not self.registration_number:
            self.registration_number = self.generate_registration_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
