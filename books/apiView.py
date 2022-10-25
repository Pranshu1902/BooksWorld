from django.contrib.auth.models import User
from books.models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'imageLink', 'totalPages', 'pagesRead', 'timeTaken', 'status']
        read_only_fields = ['user']
    
    # automatically assign the user to the book
    def validate(self, attrs):
        # user = User.objects.filter(username=self.context['request'].user)[0]
        attrs['user'] = self.context['request'].user
        return attrs

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'book'] # book is sent to the client to filter the comments based on book
        read_only_fields = ['user']
    
    # automatically assign the user to the comment
    def validate(self, attrs):
        # user = User.objects.filter(username=self.context['request'].user)[0]
        attrs['user'] = self.context['request'].user
        return attrs

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    # sign up new user
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

# class BookAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         posts = Book.objects.filter(user=request.user)
#         serializer = BookSerializer(posts, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         posts_serializer = BookSerializer(data=request.data)
#         if posts_serializer.is_valid():
#             posts_serializer.save()
#             return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             print('error', posts_serializer.errors)
#             return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

class APIUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# get logged in user's details
class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
