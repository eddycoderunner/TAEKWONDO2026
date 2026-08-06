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
        DrawResult.generate_all_draws()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        DrawResult.generate_all_draws()   

    def __str__(self):
        return self.full_name

class DrawResult(models.Model):
    gender = models.CharField(max_length=10)
    weight_category = models.CharField(max_length=50)
    fixtures = models.JSONField(default=list)
    byes = models.JSONField(default=list)
    generated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['gender', 'weight_category']

    def __str__(self):
        return f"{self.gender} - {self.weight_category}"

    @classmethod
    def generate_all_draws(cls):
        weight_categories_male = [
            "-54kg Fin Weight", "-58kg Fly Weight", "-63kg Bantam Weight",
            "-68kg Feather Weight", "-74kg Light Weight", "-80kg Welter Weight",
            "-87kg Middle Weight", "+87kg Heavy Weight"
        ]
        weight_categories_female = [
            "-46kg Fin Weight", "-49kg Fly Weight", "-53kg Bantam Weight",
            "-57kg Feather Weight", "-62kg Light Weight", "-67kg Welter Weight",
            "-73kg Middle Weight", "+73kg Heavy Weight"
        ]

        for gender, categories in[('male', weight_categories_male), ('female', weight_categories_female)]:
            for category in categories:
                players = list(Registration.objects.filter(
                    gender=gender,
                    weight_category=category
                ).values('full_name', 'club_name', 'nationality', 'registration_number'))

                random.shuffle(players)
                fixtures = []
                byes = []

                if len(players) % 2 != 0:
                    byes.append(players.pop())

                for i in range(0, len(players), 2):
                    fixtures.append({
                        'player1':players[i],
                        'player2':players[i + 1],
                    })

                cls.objects.update_or_create(
                    gender=gender,
                    weight_category=category,
                    defaults={
                        'fixtures': fixtures,
                        'byes': byes,
                    }
                )






















































     

