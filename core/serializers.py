from rest_framework import serializers
from .models import User, Book, CartItem, IssuedBook, SavedForLater
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(source='book', queryset=Book.objects.all())
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'user']

class IssuedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedBook
        fields = '__all__'

class SavedForLaterSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(source='book', queryset=Book.objects.all())
    class Meta:
        model = SavedForLater
        fields = ['id', 'book_id', 'user']
