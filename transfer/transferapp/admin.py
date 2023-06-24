from django.contrib import admin
from .models import Club,Transfer,Student,SchoolAdmin
from .models import TransferFormSettings
from .forms import TransferFormSettingsForm
# Register your models here.


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'president', 'teacher' ,'id')


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_name', 'seat_number', 'student_name', 'get_original_club', 'get_desired_club', 'submission_date', 'original_club_teacher_approved_time', 'original_club_teacher_approved', 'original_club_president_approved', 'desired_club_teacher_approved', 'desired_club_president_approved','original_club_president_approved_time', 'desired_club_teacher_approved_time',
                    'desired_club_president_approved_time')
    list_filter = ('original_club', 'desired_club')
    search_fields = ('class_name', 'student_name')

    def get_original_club(self, obj):
        return obj.original_club.name

    get_original_club.short_description = '原社團'

    def get_desired_club(self, obj):
        return obj.desired_club.name

    get_desired_club.short_description = '欲轉往社團'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_club', 'class_name', 'seat_number')

@admin.register(SchoolAdmin)
class SchoolAdminAdmin(admin.ModelAdmin):
    list_display = ['admin']

@admin.register(TransferFormSettings)
class TransferFormSettingsAdmin(admin.ModelAdmin):
    form = TransferFormSettingsForm