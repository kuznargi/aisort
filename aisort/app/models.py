from django.db import models

class Detection(models.Model):
    class_name = models.TextField()
    count = models.IntegerField(default=1)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.class_name} ({self.confidence*100:.1f}%)"
