from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from statistics import mean

class PointOfInterest(models.Model):
    name = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    ratings = models.JSONField(default=list)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.external_id})"
    
    @property
    def average_rating(self):
        if not self.ratings:
            return None
        return round(mean(self.ratings), 2)
    
    class Meta:
        verbose_name = "Point of Interest"
        verbose_name_plural = "Points of Interest"
        indexes = [
            models.Index(fields=['external_id']),
            models.Index(fields=['category']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['external_id'], name='unique_external_id')
        ]