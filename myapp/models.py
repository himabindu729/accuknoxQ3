from django.db import models,transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class MainModel(models.Model):
    name = models.CharField(max_length=100)

class SignalModel(models.Model):
    main_model = models.ForeignKey(MainModel, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)

@receiver(post_save, sender=MainModel)
def create_signal_model(sender, instance, created, **kwargs):
    if created:
        SignalModel.objects.create(main_model=instance, message="Created by signal")


# by default, Django signals run in the same database transaction as the caller. 
# If the caller’s transaction rolls back, the database changes made inside the signal also roll back.
# If the transaction fails, all changes made by the signal are rolled back.
# This prevents inconsistent data in the database.
# Django ensures data consistency by making signals part of the main transaction.