from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def create_model_instance(sender, **kwargs):
    """
    Create a default 'Uncategorized' Category instance as soon as the app is run
    """
    if sender.name == "products":
        if not Category.objects.exists():
            Category.objects.create(category="Uncategorized")
