from django.shortcuts import render , redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User

def home(request):
    stc=staticcontentClass.objects.filter(key='home')
    stp=staticphotoClass.objects.filter(key='home')
    ct=contactClass.objects.all()
    return render(request,'main_app/index.html',context={"cnt":stc, "ph":stp , "c":ct})

def layout(request):
    stp=staticphotoClass.objects.filter(key='therapy')
    stpp=staticphotoClass.objects.filter(key='psycholopathy')
    stpt=staticphotoClass.objects.filter(key='test')
    return render(request,'main_app/layout.html',context={ "ph":stp, "ph":stpp, "ph":stpt}) 

def therapy(request):
    stc=staticcontentClass.objects.filter(key='therapy')
    stp=staticphotoClass.objects.filter(key='therapy')
    if (request.method=="POST"):
        f=appointmentForm(request.POST)
        if (f.is_valid):
            f.save()
       
            f=appointmentForm()
            return render(request,'main_app/therapy.html',context={ "f":f})
    else:
      f=appointmentForm()
      return render(request,'main_app/therapy.html',context={"cnt":stc, "ph":stp ,"f":f}) 

def psychopathy(request):
    stc=staticcontentClass.objects.filter(key='psycholopathy')
    stp=staticphotoClass.objects.filter(key='psycholopathy')
    return render(request,'main_app/psychopathy.html',context={"cnt":stc,"ph":stp})

def test(request):
    stc=staticcontentClass.objects.filter(key='test')
    stp=staticphotoClass.objects.filter(key='test')
    return render(request,'main_app/test.html',context={"cnt":stc,"ph":stp})

def workshop(request):
    stc=staticcontentClass.objects.filter(key='workshop')
    stp=staticphotoClass.objects.filter(key='workshop')
    ws=workshopClass.objects.all()
    cws=categorywsClass.objects.all()
    return render(request,'main_app/workshop.html',context={"cnt":stc,"ph":stp , "w":ws , "cw":cws})

def categoryw(request,adad):
    stc=staticcontentClass.objects.filter(key='workshop')
    stp=staticphotoClass.objects.filter(key='workshop')
    ws=workshopClass.objects.filter(categoryw_id=adad)
    cws=categorywsClass.objects.all()
    return render(request,'main_app/workshop.html',context={"cnt":stc,"ph":stp , "w":ws , "cw":cws})


def team(request):
    stc=staticcontentClass.objects.filter(key='team')
    stp=staticphotoClass.objects.filter(key='team')
    return render(request,'main_app/team.html',context={"cnt":stc,"ph":stp})

def about(request):
    stc=staticcontentClass.objects.filter(key='about')
    stp=staticphotoClass.objects.filter(key='about')
    return render(request,'main_app/about.html',context={"cnt":stc,"ph":stp})

def contact(request):
    if (request.method=="POST"):
        s=""
        f=contactForm(request.POST)
        if (f.is_valid):
            f.save()
            s=request.POST.get("username")+" "+ "عزیز دیدگاه شما ثبت گردید "
            f=contactForm()
            return render(request,'main_app/contact.html',context={"username":s , "f":f})
    else:
      f=contactForm()
      return render(request,'main_app/contact.html',context={"f":f})


def article(request):
    return render(request,'main_app/article.html')

def gallery(request):
    return render(request,'main_app/gallery.html')

def rules(request):
    return render(request,'main_app/rules.html')

def register(request):
    return render(request,'main_app/register.html')

# def register(request):
#     if (request.method=="POST"):
#         f=registerForm(request.POST)
#         username=request.POST.get("usename")
#         fname=request.POST.get("fname")
#         lname=request.POST.get("lname")
#         email=request.POST.get("email")
#         mobile=request.POST.get("mobile")
#         address=request.POST.get("address")
#         passw=request.POST.get("passw")
       
#         User.objects.create_user(username,email,passw,first_name=fname,last_name=lname,mobile=mobile,address=address,is_staff=False)
        
#     return redirect("/login/")
