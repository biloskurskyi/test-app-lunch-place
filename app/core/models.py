from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user = self.model(email=email, **extra_fields)
        user.set_is_active(False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields['user_type'] = 0

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        extra_fields.pop('username', None)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    EMPLOYEE_USER = 0
    RESTAURANT_USER = 1
    POST_TYPE = ((EMPLOYEE_USER, 'EMPLOYEE USER'), (RESTAURANT_USER, 'RESTAURANT USER'),)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    user_type = models.SmallIntegerField(choices=POST_TYPE)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        if self.user_type == 0:
            return f"{self.name} with email {self.email}"
        elif self.user_type == 1:
            return f"{self.name}"


class Lunch(models.Model):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    WEEK_DAYS = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )

    menu = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    day = models.SmallIntegerField(choices=WEEK_DAYS)

    class Meta:
        verbose_name = "Lunch"
        verbose_name_plural = "Lunch menu"
        unique_together = ('user', 'day')

    def __str__(self):
        return f"restaurant {self.user} with {self.menu} on week day {self.get_day_display()}"


class LunchVoting(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    lunch = models.ForeignKey(Lunch, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Lunch Voting"
        verbose_name_plural = "Lunch Voting"
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user} voted for {self.lunch} on {self.date}"


class LunchReport(models.Model):
    lunch = models.ForeignKey(Lunch, on_delete=models.PROTECT)
    date = models.DateField()
    count = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Lunch Report"
        verbose_name_plural = "Lunch Reports"
        unique_together = ('lunch', 'date')

    def __str__(self):
        return f"{self.lunch} on {self.date} has {self.count} votes"
