from django.contrib import admin
from .models import Project, Plant, WateringLog, WateringNotificationSubscription

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'site')
    search_fields = ('name', 'description')
    list_filter = ('site',)
    ordering = ('name',)

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'recommended_watering_interval', 'created_by', 'created_at', 'archived')
    search_fields = ('name', 'description')
    list_filter = ('project', 'archived')
    ordering = ('name',)

@admin.register(WateringLog)
class WateringLogAdmin(admin.ModelAdmin):
    list_display = ('plant', 'watered_at', 'watered_by')
    search_fields = ('plant__name',)
    list_filter = ('watered_at', 'watered_by')
    ordering = ('-watered_at',)

@admin.register(WateringNotificationSubscription)
class WateringNotificationSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plant', 'subscribed_at')
    search_fields = ('user__username', 'plant__name')
    list_filter = ('subscribed_at',)
    ordering = ('-subscribed_at',)