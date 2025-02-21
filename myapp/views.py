from django.shortcuts import render,HttpResponse
from .models import MainModel, SignalModel 
from django.db import transaction

# Create your views here. 

def transaction_test_view(request):
    try:
        with transaction.atomic(): 
            MainModel.objects.create(name='Test User')  
            raise Exception("Rollback!")  
    except Exception:
        pass  

    return HttpResponse(
        f"MainModel exists: {MainModel.objects.exists()}<br>"
        f"SignalModel exists: {SignalModel.objects.exists()}"
    )

