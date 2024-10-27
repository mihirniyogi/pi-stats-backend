from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import get_gen_stats, get_cpu_stats, get_mem_stats, get_disk_stats, get_svc_stats

@api_view(['GET'])
def gen_stats(request):
  return Response(get_gen_stats())

@api_view(['GET'])
def cpu_stats(request):
  return Response(get_cpu_stats())

@api_view(['GET'])
def mem_stats(request):
  return Response(get_mem_stats())

@api_view(['GET'])
def disk_stats(request):
  return Response(get_disk_stats())

@api_view(['GET'])
def svc_stats(request):
  return Response(get_svc_stats())