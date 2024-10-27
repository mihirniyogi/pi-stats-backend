from django.urls import path
from . import views

urlpatterns = [
  path('gen/', views.gen_stats),
  path('cpu/', views.cpu_stats),
  path('mem/', views.mem_stats),
  path('disk/', views.disk_stats),
  path('svc/', views.svc_stats)
]