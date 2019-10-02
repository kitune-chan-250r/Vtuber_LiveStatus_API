from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Vtuber, On_Live
from .serializers import *
from rest_framework.decorators import api_view, permission_classes

#filter 
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

#token auth
from rest_framework.permissions import IsAuthenticated, AllowAny


"""
@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        snippets = Vtuber.objects.all()
        serializer = VtuberSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = VtuberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

"""

class VtuberList(APIView):
    
    def get(self, request, format=None):
        snippets = Vtuber.objects.all()
        serializer = VtuberSerializer(snippets, many=True)
        return Response(serializer.data)

    
    def post(self, request, format=None):
        serializer = VtuberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def snippet_detail(request, pk):
    try:
        snippet = Vtuber.objects.get(pk=pk)
    except Vtuber.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = VtuberSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = VtuberSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

class OnLiveList(APIView):
    def get(self, request, format=None):
        snippets = On_Live.objects.all()
        serializer = OnLive_POST_Serializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OnLive_POST_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OnLiveDetail(APIView):
    
    def get_object(self, pk):
        try:
            return On_Live.objects.get(pk=pk)
        except On_Live.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = OnLiveSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = OnLiveSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#?pr=[production name]で検索可能に
class OnLiveListView(generics.ListCreateAPIView):
    queryset = On_Live.objects.all()
    serializer_class = OnLiveSerializer
    permission_classes = (AllowAny, )
    def get_queryset(self):
        queryset = On_Live.objects.all()
        pr = self.request.query_params.get('pr', None)
        if pr is not None:
            queryset = queryset.filter(uid__production=pr)
        return queryset