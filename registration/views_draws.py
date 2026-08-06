from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Registration, DrawResult

@staff_member_required
def draws_view(request):
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

    male_draws = {}
    female_draws = {}

    for category in weight_categories_male:
        count = Registration.objects.filter(gender='male', weight_category=category).count()
        if count>0:
            try:
                draw = DrawResult.objects.get(gender='male', weight_category=category)
                male_draws[category]={
                    'fixtures':draw.fixtures,
                    'byes':draw.byes,
                    'count':count,
                    'generated_at':draw.generated_at,
                }
            except DrawResult.DoesNotExist:
                pass

    for category in weight_categories_female:
        count = Registration.objects.filter(gender='female', weight_category=category).count()
        if count > 0:
            try:
                draw = DrawResult.objects.get(gender='female', weight_category=category)
                female_draws[category] = {
                    'fixtures': draw.fixtures,
                    'byes': draw.byes,
                    'count': count,
                    'generated_at': draw.generated_at,
                }
            except DrawResult.DoesNotExist:
                pass

    context = {
        'male_draws': male_draws,
        'female_draws': female_draws,
    }
    return render(request, 'registration/draws.html', context)

































































