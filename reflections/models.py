from django.db import models
from accounts.models import Profile  # Assuming Profile is in accounts app


class Reflection(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reflections')
    title = models.CharField(max_length=255)
    ayah = models.TextField()
    reflection = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('reflection-detail', args=[str(self.id)])
