from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Club(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    president = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='president_clubs')
    teacher = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='teacher_clubs')

    def __str__(self):
        return self.name


class Student(models.Model):
    student_club = models.ForeignKey(Club, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=50)
    seat_number = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class SchoolAdmin(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.use.username
    
class Transfer(models.Model):
    class_name = models.CharField(max_length=50)
    seat_number = models.CharField(max_length=50)
    student_name = models.CharField(max_length=100)
    original_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='original_transfers')
    desired_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='desired_transfers')
    submission_date = models.DateTimeField(auto_now_add=True)
    original_club_teacher_approved = models.BooleanField(null=True)
    original_club_president_approved = models.BooleanField(null=True)
    desired_club_teacher_approved = models.BooleanField(null=True)
    desired_club_president_approved = models.BooleanField(null=True)
    original_club_teacher_approved_time = models.DateTimeField(null=True)
    original_club_president_approved_time = models.DateTimeField(null=True)
    desired_club_teacher_approved_time = models.DateTimeField(null=True)
    desired_club_president_approved_time = models.DateTimeField(null=True)
    
    def __str__(self):
        return f'Transfer #{self.id}'

    def is_approved(self):
        return (
        self.original_club_teacher_approved is not None
        and self.original_club_president_approved is not None
        and self.desired_club_teacher_approved is not None
        and self.desired_club_president_approved is not None
    )
    
class TransferFormSettings(models.Model):
    start_time = models.DateTimeField(verbose_name='開始時間')
    end_time = models.DateTimeField(verbose_name='結束時間')

    def __str__(self):
        return '轉社單填寫時間設置'   

