from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, blank=True)

    objects = models.Manager()
    on_site = CurrentSiteManager("site")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['name']


class Plant(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    recommended_watering_interval = models.IntegerField(
        help_text="Recommended watering interval in days"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False, help_text="Indicates if the plant is archived")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Plant"
        verbose_name_plural = "Plants"
        ordering = ['name']


class WateringLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    watered_at = models.DateTimeField(auto_now_add=True)
    watered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watering_logs')
    image = models.ImageField(upload_to='watering_logs/', blank=True, null=True)

    def __str__(self):
        return f"Watered {self.plant.name} on {self.watered_at}"

    class Meta:
        verbose_name = "Watering Log"
        verbose_name_plural = "Watering Logs"
        ordering = ['-watered_at']
        indexes = [
            models.Index(fields=['plant', 'watered_at']),
        ]


class WateringNotificationSubscription(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} subscribed to {self.plant.name}"

    class Meta:
        verbose_name = "Watering Notification Subscription"
        verbose_name_plural = "Watering Notification Subscriptions"
        unique_together = ('user', 'plant')
        ordering = ['-subscribed_at']


class WateringNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    notification_time = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        return f"Notification for {self.plant.name} at {self.notification_time}"

    class Meta:
        verbose_name = "Watering Notification"
        verbose_name_plural = "Watering Notifications"
        ordering = ['-notification_time']
        indexes = [
            models.Index(fields=['plant', 'notification_time']),
        ]