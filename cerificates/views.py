from django.shortcuts import render
from .models import Certificate

# Create your views here.
def home(request):
    certificates = Certificate.objects.all()
    return render(request, 'index.html', {'certificates': certificates})
