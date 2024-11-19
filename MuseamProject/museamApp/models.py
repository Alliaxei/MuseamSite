from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Permission, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('The Login field must be set')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser, PermissionsMixin):
    login = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default='')
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True, default=None)
    email = models.EmailField(default=None)
    username = models.CharField(max_length=255, default=0, unique=False)
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date joined'
    )

    # Уникальные related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Уникальное имя
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Уникальное имя
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.login

class Hall(models.Model):
    THEMATIC_CHOICES = [
        ('history', 'История'),
        ('art', 'Искусство'),
        ('science', 'Наука'),
        ('ethnography', 'Этнография'),
        ('archeology', 'Археология'),
        ('technology', 'Технологии'),
        ('natural_history', 'Природоведение'),
    ]

    number = models.IntegerField(unique=True, default=0)
    thematic = models.CharField(max_length=255, choices=THEMATIC_CHOICES, default='history')

    def __str__(self):
        return str(self.number)

class Exhibit(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    quantity = models.IntegerField()
    category = models.CharField(max_length=255, choices=[
        ('utensils', 'Бытовая утварь'),
        ('clothing', 'Одежда'),
        ('weapons', 'Оружие'),
        ('art', 'Живопись')
    ])
    history = models.TextField()
    condition = models.CharField(max_length=255, choices=[
        ('good', 'Хорошее'),
        ('restoration_needed', 'Требует реставрации')
    ])
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='exhibits', null=True, blank=True, default=None)

    def __str__(self):
        return self.name

class Report(models.Model):
    report_type = models.CharField(
        max_length=255,
        choices=[
            ('by_hall', 'Отчёт по содержимому выставочных залов'),
            ('by_theme', 'Отчёт по экспонатам по данной тематике'),
            ('count_by_theme', 'Отчёт о количестве экспонатов по данной тематике'),
            ('restoration', 'Отчёт по экспонатам, требующим реставрацию'),
        ]
    )
    description = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, models.SET_NULL, null=True)

    def __str__(self):
        return self.description