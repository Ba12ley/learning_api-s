from django.shortcuts import render
from rest_framework.views import APIView #a wrapper for class based api views
from rest_framework.decorators import api_view #a wrapper for function based api views goto line 64
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

class PostView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        # if serializer.is_valid():
        return Response(serializer.data)


# decorated for csrf exemption
@csrf_exempt
def post_list(request):
    if request.method == 'GET':
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False) #false, because only dictionary maybe serialized.  This will be an ordered dict

    if request.method == 'POST':
        data = JSONParser.parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
# decorated for csrf exemption
@csrf_exempt
def post_detail(request, pk):

    # try catch to see if post exists
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=400)
# statements to get type of request
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser(request)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse(status=204)

@api_view(['GET', 'POST']) #pass in here the request methods you wish to deal with
def exampleOfWrapper(request):
    if request.method == 'GET':
        pass