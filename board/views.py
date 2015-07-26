from django.shortcuts import render


def index(request):
    return render(request, 'skeleton/job_list.html')