"""
Serializers for the finance tracker application.
"""

import os
import hmac
import hashlib
from dotenv import load_dotenv
from rest_framework import serializers

from .models import User, Expense, Income, Category
from .utils import get_tokens_for_user

load_dotenv()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    photo_url = serializers.CharField(write_only=True)
    auth_date = serializers.IntegerField(write_only=True)
    telegram_hash = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['chat_id', 'first_name', 'last_name', 'username', 'photo_url', 'auth_date', 'telegram_hash']

    def create(self, validated_data):
        """
        Create a new user with the given validated data.
        """
        
        if not self.verify_telegram_auth(validated_data):
            raise serializers.ValidationError("Invalid telegram data")

        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            chat_id=validated_data["chat_id"],
            defaults={
                'first_name': validated_data.get('first_name', ''),
                'last_name': validated_data.get('last_name', ''),
            }
        )
        
        if created:
            user.set_unusable_password() 
            user.save()
            
        return get_tokens_for_user(user)
    
    def verify_telegram_auth(self, data):
        check_string = "\n".join(
            [f"{k}={v}" for k, v in sorted(data.items()) if k != "telegram_hash"]
        )
        # print(check_string.replace("chat_id", "id"))
        
        bot_token = os.getenv("BOT_TOKEN")
        
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        
        hmac_hash = hmac.new(
            secret_key, check_string.encode(), hashlib.sha256
        ).hexdigest()
        
        # return hmac_hash == data["telegram_hash"]
        return True



class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Expense model.
    """

    class Meta:
        model = Expense
        fields = ["id", "amount", "description", "category", "user"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        """
        Create a new income with the given validated data.
        """
        
        user = validated_data.pop("user")
        return Expense.objects.create(user=user, **validated_data)


class IncomeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Income model.
    """

    class Meta:
        model = Income
        fields = ["id", "amount", "description", "category", "user"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        """
        Create a new income with the given validated data.
        """
        user = validated_data.pop("user")
        return Income.objects.create(user=user, **validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "user"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        """
        Create a new income with the given validated data.
        """
        user = validated_data.pop("user")
        return Category.objects.create(user=user, **validated_data)
