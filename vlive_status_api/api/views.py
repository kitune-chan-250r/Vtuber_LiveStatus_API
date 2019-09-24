from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Vtuber, On_Live
from .serializers import VtuberSerializer, OnLiveSerializer
from rest_framework.decorators import api_view

#filter 
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics


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
        serializer = OnLiveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


#onlive_detail
@api_view(['GET', 'PUT', 'DELETE'])
def onlive_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = On_Live.objects.get(pk=pk)
    except On_Live.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OnLiveSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OnLiveSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
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