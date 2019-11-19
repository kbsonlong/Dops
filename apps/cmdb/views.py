from django.shortcuts import render

# Create your views here.

from . import models

def index(request):
    product = models.Product.objects.first()

    return render(request,"index.html",{"product":product})


def chart(request,id):
    product = models.Product.objects.filter(id=id)

    return render(request, "index.html", {"product": product})