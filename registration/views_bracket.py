from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Registration, DrawResult, BracketResult
from .bracket import get_flag, build_bracket
import json

@staff_member_required
def bracket_view(request):
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

    male_categories = []
    female_categories = []

    for category in weight_categories_male:
        count = Registration.objects.filter(gender='male', weight_category=category).count()
        if count > 0:
            male_categories.append(category)

    for category in weight_categories_female:
        count = Registration.objects.filter(gender='female', weight_category=category).count()
        if count > 0:
            female_categories.append(category)

    context = {
        'male_categories': male_categories,
        'female_categories': female_categories,
    }
    return render(request, 'registration/bracket.html', context)


@staff_member_required
def get_bracket_data(request):
    gender = request.GET.get('gender')
    category = request.GET.get('category')

    try:
        draw = DrawResult.objects.get(gender=gender, weight_category=category)
        players = list(Registration.objects.filter(
            gender=gender,
            weight_category=category
        ).values('full_name', 'club_name', 'nationality', 'registration_number'))


        for p in players:
            p['flag'] = get_flag(p['nationality'])

        for b in draw.byes:
            b['flag'] = get_flag(b.get('nationality', ''))


        try:
            saved = BracketResult.objects.get(gender=gender, weight_category=category)
            bracket_data = saved.bracket_data
        except BracketResult.DoesNotExist:
            bracket_data = {}

        return JsonResponse({
            'status': 'success',
            'fixtures': draw.fixtures,
            'byes': draw.byes,
            'players': players,
            'bracket_data': bracket_data,
            'category': category,
            'gender': gender,
        })

    except DrawResult.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No draw found'})


@staff_member_required
def save_bracket(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            gender = data.get('gender')
            category = data.get('category')
            bracket_data = data.get('bracket_data', {})

            BracketResult.objects.update_or_create(
                gender=gender,
                weight_category=category,
                defaults={'bracket_data': bracket_data}
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})