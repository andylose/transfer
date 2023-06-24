from django.shortcuts import render, redirect     
from django.contrib.auth.forms import AuthenticationForm
from .models import Club, Transfer, Student, SchoolAdmin, TransferFormSettings
from django.contrib.auth import login
from .forms import TransferForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.

#主頁
def homepage(request):
    return render(request, 'transferapp/homepage.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/serve/')  
    else:
        form = AuthenticationForm()
    return render(request, 'transferapp/login.html', {'form': form})

#登入
@login_required
def serve(request):
    user = request.user

    if Student.objects.filter(user=user).exists():
        return render(request, 'transferapp/student_serve.html')
    elif SchoolAdmin.objects.filter(admin=user).exists():
        return render(request, 'transferapp/school_admin_serve.html')
    elif Club.objects.filter(president=user).exists() or Club.objects.filter(teacher=user).exists():
        return render(request, 'transferapp/teacher_serve.html')
    else:
        return render(request, 'transferapp/serve.html')

#學生主頁
def student_serve(request):
    return render(request, 'transferapp/student_serve.html')

#老師/社長主頁
def teacher_serve(request):
    return render(request, 'transferapp/teacher_serve.html')

#學務處主頁
def school_admin_serve(request):
    return render(request, 'transferapp/school_admin_serve.html')

#錯誤介面
def error_2 (request):
    return render(request, 'transferapp/error_2.html')

#轉社單
def transfer_form(request):
    current_time = timezone.now()
    settings = TransferFormSettings.objects.first()

    if not settings or not settings.start_time or not settings.end_time:
        return redirect('error_page')

    if current_time < settings.start_time or current_time > settings.end_time:
        return redirect('error_page')

    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
            if Transfer.objects.filter(student_name=student.user.username).exists():
                return redirect('already_filled')
        except Student.DoesNotExist:
            return redirect('error_2')

    clubs = Club.objects.all()

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.student_name = student.user.username
            transfer.save()
            return redirect('serve')
    else:
        form = TransferForm()

    return render(request, 'transferapp/transfer_form.html', {'form': form, 'clubs': clubs})


#已填過轉社單
def already_filled(request):
    return render(request, 'transferapp/already_filled.html')

#審核轉社單主頁
@login_required
def check_transfer_form_approval(request):
    user = request.user
    clubs = Club.objects.filter(teacher=user) | Club.objects.filter(president=user)
    club_ids = clubs.values_list('id', flat=True)

    original_club_transfers = Transfer.objects.filter(original_club_id__in=club_ids)
    desired_club_transfers = Transfer.objects.filter(desired_club_id__in=club_ids) 
    
    transfer_forms = original_club_transfers.union(desired_club_transfers)

    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        action = request.POST.get('action')

        if form_id and action:
            transfer_form = Transfer.objects.get(id=form_id)

            if user == transfer_form.original_club.president and not transfer_form.original_club_president_approved:
                if action == 'approve':
                    transfer_form.original_club_president_approved = True
                    transfer_form.original_club_president_approved_time = timezone.now()
                    transfer_form.save()
                    
                elif action == 'reject':
                    transfer_form.original_club_president_approved = False
                    transfer_form.original_club_president_approved_time = timezone.now()
                    transfer_form.save()
                    

            elif user == transfer_form.original_club.teacher and not transfer_form.original_club_teacher_approved:
                if action == 'approve':
                    transfer_form.original_club_teacher_approved = True
                    transfer_form.original_club_teacher_approved_time = timezone.now()
                    transfer_form.save()
                    
                elif action == 'reject':
                    transfer_form.original_club_teacher_approved = False
                    transfer_form.original_club_teacher_approved_time = timezone.now()
                    transfer_form.save()
                    

            elif user == transfer_form.desired_club.president and not transfer_form.desired_club_president_approved:
                if action == 'approve':
                    transfer_form.desired_club_president_approved = True
                    transfer_form.desired_club_president_approved_time = timezone.now()
                    transfer_form.save()
                    
                elif action == 'reject':
                    transfer_form.desired_club_president_approved = False
                    transfer_form.desired_club_president_approved_time = timezone.now()
                    transfer_form.save()
                    

            elif user == transfer_form.desired_club.teacher and not transfer_form.desired_club_teacher_approved:
                if action == 'approve':
                    transfer_form.desired_club_teacher_approved = True
                    transfer_form.desired_club_teacher_approved_time = timezone.now()
                    transfer_form.save()
                    
                elif action == 'reject':
                    transfer_form.desired_club_teacher_approved = False
                    transfer_form.desired_club_teacher_approved_time = timezone.now()
                    transfer_form.save()
                    

    return render(request, 'transferapp/check_transfer_form_approval.html', {'transfer_forms': transfer_forms, 'user': user})

#查看轉社單進度
def check_transfer_form_progress(request):
    transfers = Transfer.objects.all()
    return render(request, 'transferapp/check_transfer_form_progress.html', {'transfers': transfers})

#最終審核
def final_check(request):
    approved_forms = Transfer.objects.filter(
        original_club_teacher_approved=True,
        original_club_president_approved=True,
        desired_club_teacher_approved=True,
        desired_club_president_approved=True
    )
    
    return render(request, 'transferapp/final_check.html', {'approved_forms': approved_forms})

#錯誤頁面
def error_page(request):
    return render(request, 'transferapp/error_page.html')


    


