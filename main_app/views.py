from django.shortcuts import render , redirect
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login as lg , logout as lo
from django.http import JsonResponse


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
        fullname=" "
        f=appointmentForm(request.POST)
        if (f.is_valid): 
            f.save()
            fullname=request.POST.get("fullname" )+" "+" عزیز نوبت شما با موفقیت ثبت گردید"
            f=appointmentForm()
            return render(request,'main_app/therapy.html',context={ "f":f , "fullname":fullname ,"cnt":stc, "ph":stp })
    else:
      f=appointmentForm()
      return render(request,'main_app/therapy.html',context={"cnt":stc, "ph":stp ,"f":f}) 



def psychopathy(request):
    stc=staticcontentClass.objects.filter(key='psycholopathy')
    stp=staticphotoClass.objects.filter(key='psycholopathy')
    if (request.method=="POST"):
        fullname=" "
        f=appointmentForm2(request.POST)
        if (f.is_valid): 
            f.save()
            fullname=request.POST.get("fullname" )+" "+" عزیز نوبت شما با موفقیت ثبت گردید"
            f=appointmentForm2()
            return render(request,'main_app/psychopathy.html',context={ "f":f , "fullname":fullname,"cnt":stc, "ph":stp })
    else:
        f=appointmentForm2()
    return render(request,'main_app/psychopathy.html',context={"cnt":stc,"ph":stp ,"f":f})

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
    if (request.method=="POST"):
        username=request.POST.get("username")
        lname=request.POST.get("lname")
        fname=request.POST.get("fname")
        email=request.POST.get("email")
        passw=request.POST.get("passw")
        customuserClass.objects.create_user(username,email,passw,last_name=lname,first_name=fname,is_staff=False)
        return redirect("/login/")

    return render(request,'main_app/register.html')

@login_required 
def dashboard(request):
    if (request.user.rolle=="therapeutist"):
        return render(request,'main_app/dashboard.html')
    else:
        return redirect("/panel/")

@login_required 
def panel(request):
    if (request.user.rolle=="client"):
        return render(request,'main_app/userpanel.html')
    else:
        return redirect("/dashboard/")


def logout(request):
    lo(request)
    return redirect("/login/")

def login(request):
    if (request.method=="POST"):
        username=request.POST.get("username")
        passw=request.POST.get("passw")
        u=authenticate(username=username,password=passw)
        if u is not None:
            lg(request,u)
            if  (u.rolle=="therapeutist"):
                return redirect("/dashboard/")
            else:
                return redirect("/panel/")

        else:
                return render(request,'main_app/login.html' ,context={"massage":"نام کاربری یا رمز عبور اشتباه است"})
    else:
        return render(request,'main_app/login.html')
    
    
def reserve(request):
    return render(request,'main_app/reserve.html')
 
 
def get_schedule_by_therapist(request):
    therapist_id = request.GET.get("therapist_id")
    if therapist_id:
        schedules = scheduleClass.objects.filter(therapeutist_id=therapist_id)
        data = [
            {
                "id": schedule.id,
                "date": schedule.date.strftime("%Y-%m-%d"),
                "start_time": schedule.start_time.strftime("%H:%M"),
                "end_time": schedule.end_time.strftime("%H:%M"),
            }
            for schedule in schedules
        ]
        return JsonResponse({"schedules": data})
    return JsonResponse({"schedules": []})



