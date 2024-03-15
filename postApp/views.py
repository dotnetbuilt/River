from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response

@api_view(['GET'])
def get_all_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success":"Post was created"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post(request):
    post_id = request.data['post_id'] 
    try:
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_post(request):
    post_id = request.data['post_id'] 
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response({"Success":"Post was successfully deleted"}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({"Detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
def update_post(request):
    post_id = request.data['id']
    new_title = request.data['title']
    new_content = request.data['content']
    try:
        post = Post.objects.get(id=post_id)
        if new_title:
            post.title = new_title
        if new_content:
            post.content = new_content
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({"Detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)