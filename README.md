Do Django Signals Run in the Same Database Transaction as the Caller?

Django signals allow different parts of an application to communicate.Django Signals Run in the Same Database Transaction as the Caller.
By default, Django signals run within the same database transaction as the function that triggered them. This means that if the main transaction fails or rolls back, any database operations performed inside the signal handler are also rolled back, ensuring data consistency.

Proof with a Code Snippet. The following code demonstrates this behavior:

from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

# Define models
class MainModel(models.Model):
    name = models.CharField(max_length=100)

class SignalModel(models.Model):
    main_model = models.ForeignKey(MainModel, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)

# Signal handler
@receiver(post_save, sender=MainModel)
def create_signal_model(sender, instance, created, **kwargs):
    if created:
        SignalModel.objects.create(main_model=instance, message="Created by signal")

View to Test Transaction Behavior

from django.shortcuts import render, HttpResponse
from .models import MainModel, SignalModel
from django.db import transaction

# View to test transaction rollback

def transaction_test_view(request):
    try:
        with transaction.atomic():
            MainModel.objects.create(name='Test User')  
            raise Exception("Rollback!")  # Force a rollback
    except Exception:
        pass  
     return HttpResponse(
        f"MainModel exists: {MainModel.objects.exists()}<br>"
        f"SignalModel exists: {SignalModel.objects.exists()}"
    )

Expected Behavior

If Django signals were independent of the main transaction, SignalModel would still have entries even if MainModel failed. However, since Django ensures that signals run in the same transaction, we expect both MainModel and SignalModel to roll back.

Expected Output in Browser

MainModel exists: True
SignalModel exists: True

Since the exception caused a rollback, but the signal handler executed outside the transaction, the records in MainModel and SignalModel still exist. This proves that Django signals may not always be transaction-bound unless explicitly handled.

Conclusion:
Django signals are transaction-bound, meaning:They execute within the same database transaction as the caller.
If the caller’s transaction is committed, the signal’s changes persist.If the caller’s transaction rolls back, any changes made inside the signal handler also roll back.
This behavior helps prevent inconsistent data and ensures data integrity.
