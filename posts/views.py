from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView #a wrapper for class based api views
from rest_framework.decorators import api_view #a wrapper for function based api views goto line 64
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .serializers import PostSerializer, OwnerSerializer
from .models import Post
from rest_framework.parsers import JSONParser
from .permissions import IsOwnerPermission # custom permissions added in permissions.py use in the class based view
from django.contrib.auth import get_user_model

User = get_user_model()

class PostView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        # if serializer.is_valid():
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data) # using data not post
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):

        # try catch to see if post exists
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return HttpResponse(status=400)


        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return HttpResponse(status=400)
        post.delete()
        return Response(status=HTTP_204_NO_CONTENT)


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


# @api_view(['GET', 'POST']) #pass in here the request methods you wish to deal with
# def exampleOfWrapper(request):
#     if request.method == 'GET':
#         pass

@api_view(['GET', 'POST']) #pass in here the request methods you wish to deal with
def exampleOfWrapper(request):
    if request.method == 'GET':
        pass

#add in the mixin arguement before the generics.  The mixin allows to inherit methods from the mixin classes, multiple mixins can be used
class PostMixinListView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    #using the mixin removes the repitition of the below code
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

# using generic view available, looks like below and the names give away the view.  Django reduces the logic for CRUD
#generics have a useful permission_classes built in.  import from rest_framework.permissions
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwnerPermission )

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwnerPermission)

class PostDestroView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class OwnerDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = OwnerSerializer

#This gives all the views created above, but in a generic manner.  See urls.py for routing
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny, )