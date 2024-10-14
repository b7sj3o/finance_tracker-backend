from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator
from decimal import Decimal

class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None):
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None):
        user = self.model(username=username)
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    chat_id = models.CharField(max_length=300, unique=True)
    balance = models.FloatField(default=0)

    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def update_balance(self) -> float:
        expenses = sum(expense.amount for expense in self.expense_set.all())
        incomes = sum(income.amount for income in self.income_set.all())

        self.balance = round(incomes - expenses, 2)
        self.save()

        return self.balance

    def __str__(self) -> str:
        return self.username


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name.capitalize()}"


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0.01))]
    )
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount} by {self.user}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0.01))]
    )
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount} by {self.user}"
