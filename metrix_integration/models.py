from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    metrix_id = models.IntegerField(unique=True)
    metrix_code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.user.username

class MetrixUserMapping(models.Model):
    metrix_user_id = models.IntegerField(unique=True)
    your_app_user = models.OneToOneField(User, on_delete=models.CASCADE)


class Result(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    competition_id = models.IntegerField()
    date = models.DateField(null=True, blank=True)
    hole_number = models.IntegerField(null=True, blank=True)
    hole_result = models.IntegerField(null=True, blank=True)
    hole_diff = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} - {self.course} - Hole {self.hole_number} - {self.hole_result}"


class Course(models.Model):
    name = models.CharField(max_length=255)
    course_id = models.IntegerField(unique=True, blank=True, null=True)
    par = models.IntegerField(unique=True)


class Statistics(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    total_competitions = models.IntegerField(default=0)
    total_throws = models.IntegerField(default=0)
    total_difference_to_par = models.IntegerField(default=0)

    def __str__(self):
        return str(self.member)
