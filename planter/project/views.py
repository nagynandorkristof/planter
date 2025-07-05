from django.shortcuts import render
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site # Remove
from django.shortcuts import get_object_or_404, redirect
from .models import Project, Plant, WateringLog, WateringNotificationSubscription
from django.utils import timezone
from django.http import HttpResponseForbidden
from .forms import WaterPlantForm

# Create your views here.
# Functionalities:
# 1. Add plant to project
# 2. Archive plant
# 3. View all plants in a project and the last watered date
# 4. View plant details - including watering history
# 5. Water a plant in the details view
# 6. Subscribe to watering reminders for a plant in the details view
# 7. Un-subscribe from watering reminders for a plant in the details view

# Use class based views for better organization and readability
# Use Django's built-in generic views where applicable

# ! It's a multisite project, so we need to handle sites properly




class PlantListView(LoginRequiredMixin, generic.ListView):
    model = Plant
    template_name = 'project/plants/plants_list.html'
    context_object_name = 'plants'

    def get_queryset(self):
        site = get_current_site(self.request)
        return Plant.objects.filter(project__site=site, archived=False).order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, site=get_current_site(self.request))
        context['water_plant_form'] = WaterPlantForm()
        # last_watered dictionary minden növényhez
        context['last_watered'] = {
            plant.id: WateringLog.objects.filter(plant=plant).order_by('-watered_at').first()
            for plant in context['plants']
        }
        return context

class PlantDetailView(LoginRequiredMixin, generic.DetailView):
    model = Plant
    template_name = 'project/plants/plant_detail.html'
    context_object_name = 'plant'

    def get_queryset(self):
        site = get_current_site(self.request)
        return Plant.objects.filter(project__site=site)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plant = self.object
        context['watering_logs'] = WateringLog.objects.filter(plant=plant).order_by('-watered_at')
        context['subscribed'] = WateringNotificationSubscription.objects.filter(
            user=self.request.user, plant=plant
        ).exists()
        context['water_plant_form'] = WaterPlantForm()
        return context

class PlantCreateView(LoginRequiredMixin, generic.CreateView):
    model = Plant
    fields = ['name', 'description', 'image', 'recommended_watering_interval']
    template_name = 'plants/plant_form.html'

    def form_valid(self, form):
        project = get_object_or_404(Project, site=get_current_site(self.request))
        form.instance.project = project
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('plants:plant-list', kwargs={'project_id': self.kwargs['project_id']})

class PlantArchiveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        plant = get_object_or_404(Plant, id=kwargs['pk'], project__site=get_current_site(request))
        if plant.created_by != request.user and not request.user.is_superuser:
            return HttpResponseForbidden()
        plant.archived = True
        plant.save()
        return redirect('plants:plant-list', project_id=plant.project.id)

class WaterPlantView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        plant = get_object_or_404(Plant, id=kwargs['pk'], project__site=get_current_site(request))
        form = WaterPlantForm(request.POST, request.FILES)
        if form.is_valid():
            watering_log = form.save(commit=False)
            watering_log.plant = plant
            watering_log.watered_by = request.user
            watering_log.watered_at = timezone.now()
            watering_log.save()
        return redirect('plants:plant-detail', pk=plant.id)

class SubscribeWateringReminderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        plant = get_object_or_404(Plant, id=kwargs['pk'], project__site=get_current_site(request))
        WateringNotificationSubscription.objects.get_or_create(user=request.user, plant=plant)
        return redirect('plants:plant-detail', pk=plant.id)

class UnsubscribeWateringReminderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        plant = get_object_or_404(Plant, id=kwargs['pk'], project__site=get_current_site(request))
        WateringNotificationSubscription.objects.filter(user=request.user, plant=plant).delete()
        return redirect('plants:plant-detail', pk=plant.id)
    
# APIS

from .serializers import PlantSerializer, ProjectSerializer, WateringLogSerializer, WateringSerializer, SubscriptionSerializer
from rest_framework import generics, permissions
from django.http import HttpResponseForbidden
from rest_framework.response import Response

class CurrentProjectAPIView(generics.RetrieveAPIView):
    """
    Retrieves the current project for the site associated with the request.
    This view is used to get the project details for the current site.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Project, site=get_current_site(self.request))
    
class PlantListAPIView(generics.ListAPIView):
    """
    Lists all plants for the current site that are not archived.
    """
    serializer_class = PlantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Plant.objects.filter(project__site=get_current_site(self.request), archived=False)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PlantDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieves a specific plant by its ID.
    The plant must belong to the current site and must not be archived.
    """
    serializer_class = PlantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Plant.objects.filter(project__site=get_current_site(self.request), archived=False)

class WateringLogListAPIView(generics.ListAPIView):
    """
    Lists all watering logs for a specific plant.
    The plant must belong to the current site and must not be archived.
    """
    serializer_class = WateringLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        plant_id = self.kwargs['pk']
        return WateringLog.objects.filter(
            plant__id=plant_id,
            plant__project__site=get_current_site(self.request),
            plant__archived=False
        )

class WateringAPIView(generics.GenericAPIView):
    """
    Allows a user to water a plant.
    The plant must belong to the current site and must not be archived.
    """
    serializer_class = WateringSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plant = serializer.validated_data['plant']
        if plant.archived:
            return HttpResponseForbidden("Cannot water an archived plant.")
        serializer.save(watered_by=request.user)
        return Response({"status": "Plant watered successfully."})
    
class SubscriptionAPIView(generics.GenericAPIView):
    """
    Allows users to subscribe or unsubscribe to watering notifications for a specific plant.
    The plant must belong to the current site and must not be archived.
    Users can only manage their own subscriptions.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WateringNotificationSubscription.objects.filter(user=self.request.user, plant__archived=False)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription, created = WateringNotificationSubscription.objects.get_or_create(
            user=request.user,
            plant=serializer.validated_data['plant']
        )
        if created:
            return Response({"status": "Subscribed successfully."})
        return Response({"status": "Already subscribed."})

    def delete(self, request, *args, **kwargs):
        subscription = get_object_or_404(
            WateringNotificationSubscription,
            user=request.user,
            plant__id=kwargs['pk']
        )
        subscription.delete()
        return Response({"status": "Unsubscribed successfully."})