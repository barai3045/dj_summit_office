from django.shortcuts import render


# Create your views here.
def home(request):
    template_path = "home/home.html"

    context = {

    }

    return render(request, template_path, context)