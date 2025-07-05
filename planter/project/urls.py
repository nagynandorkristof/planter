from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    path('', views.PlantListView.as_view(), name='plant-list'),
    path('add/', views.PlantCreateView.as_view(), name='plant-add'),
    path('<int:pk>/', views.PlantDetailView.as_view(), name='plant-detail'),
    path('<int:pk>/archive/', views.PlantArchiveView.as_view(), name='plant-archive'),
    path('<int:pk>/water/', views.WaterPlantView.as_view(), name='plant-water'),
    path('<int:pk>/subscribe/', views.SubscribeWateringReminderView.as_view(), name='plant-subscribe'),
    path('<int:pk>/unsubscribe/', views.UnsubscribeWateringReminderView.as_view(), name='plant-unsubscribe'),
]