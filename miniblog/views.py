
from miniblog.models import MiniBlog
from miniblog.serializers import MiniBlogModelSerializer,UserModelSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view,action
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('users-list', request=request, format=format),
        'miniblogs': reverse('miniblog-list', request=request, format=format)
    })


class MiniBlogHighlight(generics.GenericAPIView):
    queryset = MiniBlog.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response(obj.highlighted)

"""
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

@csrf_exempt
def list_csrf(request):
    #get method
    if request.method == 'GET':
        #get all objects
        miniblogs = MiniBlog.objects.all()
        #
        serializer = MiniBlogModelSerializer(miniblogs, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MiniBlogModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def list_api(request):
    if request.method == 'GET':
        miniblogs = MiniBlog.objects.all()
        serializer = MiniBlogModelSerializer(miniblogs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MiniBlogModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def detail_csrf(request, pk,format=None):
    try:
        miniblog = MiniBlog.objects.get(pk=pk)
    except MiniBlog.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MiniBlogModelSerializer(miniblog)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MiniBlogModelSerializer(miniblog, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        miniblog.delete()
        return HttpResponse(status=204)

@api_view(['GET', 'PUT', 'DELETE'])
def detail_api(request, pk,format=None):
    try:
        miniblog = MiniBlog.objects.get(pk=pk)
    except MiniBlog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MiniBlogModelSerializer(miniblog)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MiniBlogModelSerializer(miniblog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        miniblog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
class MiniBlogListAPIView(APIView):
    def get(self, request, format=None):
        snippets = MiniBlog.objects.all()
        serializer = MiniBlogModelSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MiniBlogModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MiniBlogDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return MiniBlog.objects.get(pk=pk)
        except MiniBlog.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        object = self.get_object(pk)
        serializer = MiniBlogModelSerializer(object)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        object = self.get_object(pk)
        serializer = MiniBlogModelSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

######################################
class MiniBlogListMixins(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = MiniBlog.objects.all()
    serializer_class = MiniBlogModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        

class MiniBlogDetailMixins(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = MiniBlog.objects.all()
    serializer_class = MiniBlogModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

####################################################
from .permission import IsOwnerOrReadOnly
class MiniBlogList(generics.ListCreateAPIView):
    queryset = MiniBlog.objects.all()
    serializer_class = MiniBlogModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MiniBlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MiniBlog.objects.all()
    serializer_class = MiniBlogModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
###########################################################
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class MiniBlogViewSet(viewsets.ModelViewSet):
    queryset = MiniBlog.objects.all()
    serializer_class = MiniBlogModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        objs = self.get_object()
        return Response(objs.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        print()