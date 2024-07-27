from django.http import HttpResponse
import pathlib
from django.shortcuts import render
from visits.models import  PageVisit

this_dir = pathlib.Path(__file__).resolve().parent


def home_view(request,*args,**kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)


    my_title = "My Page"
    PageVisit.objects.create(path=request.path)
    my_context = {
        "page_title":"Home Page",
        "page_visit_count":page_qs.count(),
        "total_visit_count":qs.count()
    }

    html_template = "home.html"
    return render(request,html_template,my_context)






def about_view(request,*args,**kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)


    try:
        my_title = "My Page"
        PageVisit.objects.create(path=request.path)
        my_context = {
            "page_title":"Home Page",
            "page_visit_count":page_qs.count(),
            "total_visit_count":qs.count()
        }
    except:
        print("error")

    html_template = "home.html"
    return render(request,html_template,my_context)

