from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
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
            email = request.POST.get('email', '').strip()

            already_registered = Registration.objects.filter(
                full_name__iexact=full_name,
                club_name__iexact=club_name
            ).exists()

            if already_registered:
                return JsonResponse({
                    'status': 'error',
                    'field': 'duplicate',
                    'message': f'"{full_name}" from "{club_name}" has already been registered!'
                })

            email_exists = Registration.objects.filter(email__iexact=email).exists()
            if email_exists:
                return JsonResponse({
                    'status': 'error',
                    'field': 'email',
                    'message': f'This email "{email}" is already registered!'
                })

            new_player = Registration.objects.create(
                full_name=full_name,
                club_name=club_name,
                age=age,
                gender=request.POST.get('gender'),
                weight_category=request.POST.get('weight_category'),
                nationality=request.POST.get('nationality'),
                email=email,
                photo=request.FILES.get('photo'),
            )

            try:
                send_mail(
                    subject='Taekwondo Tournament Registration Confirmed',
                    message=f'''Dear {full_name},

Your registration for the Taekwondo Tournament has been confirmed!

Here are your registration details:
_________________________________________________________

Registration No : {new_player.registration_number}
Full Name       : {full_name}
Age             : {age}
Club            : {club_name}
Gender          : {request.POST.get('gender')}
Weight Category : {request.POST.get('weight_category')}
Nationality     : {request.POST.get('nationality')}

_________________________________________________________

IMPORTANT: Save your Registration Number to login and view your details:
👉 {new_player.registration_number}

Good luck and see you on the mat!

Regards,
Taekwondo Tournament Committee
@eddychamptkd''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                print("EMAIL SENT SUCCESSFULLY")
            except Exception as email_error:
                print(f"EMAIL FAILED: {email_error}")

            return JsonResponse({
                'status': 'success',
                'registration_number': new_player.registration_number,
                'full_name': full_name
            })

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'field': 'server', 'message': 'Something went wrong. Please try again.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def login_view(request):
    if request.method == 'POST':
        registration_number = request.POST.get('registration_number', '').strip().upper()

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
                'message': 'Registration number not found.'
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
                return JsonResponse({'status': 'error', 'field': 'age', 'message': 'Sorry! You must be between 15 and 40 years.'})

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
            return JsonResponse({'status': 'error', 'message': 'Something went wrong. Please try again.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



def athletes_list(request):
    if request.method == 'GET':
        athletes = Registration.objects.all().order_by('full_name')
        data = []
        for athlete in athletes:
            data.append({
                'full_name': athlete.full_name,
                'club_name': athlete.club_name,
                'weight_category': athlete.weight_category,
                'nationality': athlete.nationality,
                'gender': athlete.gender,
                'photo': athlete.photo.url if athlete.photo else None,
            })
        return JsonResponse({'status': 'success', 'athletes': data})