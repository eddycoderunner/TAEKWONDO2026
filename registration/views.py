from django.shortcuts import render
from django.http import JsonResponse
from .models import Registration
import traceback

def home(request):
    return render(request, 'registration/taekwondo.html')

def register(request):
    if request.method == 'POST':
        try:
            age = int(request.POST.get('age', 0))

            if age < 15 or age > 40:
                return JsonResponse({'status': 'error', 'field': 'age', 'message': 'Sorry! You must be between 15 and 40 years.'})

            full_name = request.POST.get('fullname', '').strip()
            club_name = request.POST.get('club_name', '').strip()

            already_registered = Registration.objects.filter(
                full_name__iexact=full_name,
                club_name__iexact=club_name
            ).exists()

            if already_registered:
                return JsonResponse({
                    'status': 'error',
                    'field': 'duplicate',
                    'message': f'⚠️ "{full_name}" from "{club_name}" has already been registered!'
                })

            new_player = Registration.objects.create(
                full_name=full_name,
                club_name=club_name,
                age=age,
                gender=request.POST.get('gender'),
                weight_category=request.POST.get('weight_category'),
                nationality=request.POST.get('nationality'),
                photo=request.FILES.get('photo'),
            )
            
            return JsonResponse({
                'status': 'success',
                'registration_number': new_player.registration_number,
                'full_name': full_name
            })

        except Exception as e:
            print(f"SERVER ERROR: {e}")
            return JsonResponse({'status': 'error', 'field': 'server', 'message': 'Something went wrong. Please try again.'})

    return render(request, 'registration/taekwondo.html')

def login_view(request):
    if request.method == 'POST':
        registration_number = request.POST.get('registration_number', '').strip()

        try:
            player = Registration.objects.get(registration_number=registration_number)
            return JsonResponse({
                'status': 'success',
                'player': {
                    'registration_number': player.registration_number,
                    'full_name': player.full_name,
                    'age': player.age,
                    'club_name': player.club_name,
                    'gender': player.gender,
                    'weight_category': player.weight_category,
                    'nationality': player.nationality,
                    'photo': player.photo.url if player.photo else None,
                }
            })
        except Registration.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': '⚠️ Registration number not found.'
            })
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def update_view(request):
    if request.method == 'POST':
        try:
            registration_number = request.POST.get('registration_number', '').strip()

            try:
                player = Registration.objects.get(registration_number=registration_number)
            except Registration.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': '⚠️ Player not found.'})
            age = int(request.POST.get('age', player.age))
            if age < 15 or age > 40:
                return JsonResponse({'status': 'error', 'field': 'age', 'message': 'Sorry!You must be between 15 and 40 years.'})
            player.full_name = request.POST.get('fullname', player.full_name).strip()
            player.age = age
            player.club_name = request.POST.get('club_name', player.club_name).strip()
            player.gender = request.POST.get('gender', player.gender)
            player.weight_category = request.POST.get('weight_category', player.weight_category)
            player.nationality = request.POST.get('nationality', player.nationality)

            if request.FILES.get('photo'):
                player.photo = request.FILES.get('photo')

            player.save()

            return JsonResponse({
                'status': 'success',
                'message': f'✅ Details updated successfully for {player.full_name}!'
            })
        
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': 'Something went wrong. pLease try again'})
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})