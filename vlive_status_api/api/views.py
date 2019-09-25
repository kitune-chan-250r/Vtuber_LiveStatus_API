from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Vtuber, On_Live
from .serializers import * #VtuberSerializer, OnLiveSerializer
from rest_framework.decorators import api_view

#filter 
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response


@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
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

@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
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


@csrf_exempt
def onlive_all(request):
    if request.method == 'GET':
        snippets = On_Live.objects.all()
        serializer = OnLiveSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OnLive_POST_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


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

    def get_queryset(self):
        queryset = On_Live.objects.all()
        pr = self.request.query_params.get('pr', None)
        if pr is not None:
            queryset = queryset.filter(uid__production=pr)
        return queryset