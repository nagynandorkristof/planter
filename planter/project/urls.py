from django.urls import path, include
from . import views

app_name = 'plants'

api_urlpatterns = [
    path('project/current/', views.CurrentProjectAPIView.as_view(), name='api-current-project'),
    path('plants/', views.PlantListAPIView.as_view(), name='api-plant-list'),
    path('plants/<int:pk>/', views.PlantDetailAPIView.as_view(), name='api-plant-detail'),
    path('plants/<int:pk>/watering-logs/', views.WateringLogListAPIView.as_view(), name='api-plant-watering-logs'),
    path('plants/<int:pk>/water/', views.WateringAPIView.as_view(), name='api-plant-water'),
    path('plants/<int:pk>/subscribe/', views.SubscribeWateringReminderView.as_view(), name='api-plant-subscribe'),
    path('plants/<int:pk>/unsubscribe/', views.UnsubscribeWateringReminderView.as_view(), name='api-plant-unsubscribe'),
]

urlpatterns = [
    path('', views.PlantListView.as_view(), name='plant-list'),
    path('add/', views.PlantCreateView.as_view(), name='plant-add'),
    path('<int:pk>/', views.PlantDetailView.as_view(), name='plant-detail'),
    path('<int:pk>/archive/', views.PlantArchiveView.as_view(), name='plant-archive'),
    path('<int:pk>/water/', views.WaterPlantView.as_view(), name='plant-water'),
    path('<int:pk>/subscribe/', views.SubscriptionAPIView.as_view(), name='plant-subscribe'),
    path('api/', include(api_urlpatterns)),
]

