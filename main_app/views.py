from django.shortcuts import render , redirect ,get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate ,login as lg , logout as lo
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages



def home(request):
    stc=staticcontentClass.objects.filter(key='home')
    stp=staticphotoClass.objects.filter(key='home')
    ct=contactClass.objects.all()[:3]
    cinfo=ClinicInfoClass.objects.all()
    if request.user.is_authenticated:
        reservation = reservationClass.objects.filter(user=request.user, status='cart')
        order=orderClass.objects.filter(user=request.user, status='cart').first()
    else:
        reservation = None
        order=None
    return render(request,'main_app/index.html',context={"cnt":stc, "ph":stp , "c":ct,"cinfo":cinfo,"reservation":reservation,"order":order})



def layout(request):
    stp=staticphotoClass.objects.filter(key='therapy')
    stpp=staticphotoClass.objects.filter(key='psycholopathy')
    stpt=staticphotoClass.objects.filter(key='test')
    return render(request,'main_app/layout.html',context={ "ph":stp, "ph":stpp, "ph":stpt}) 



@login_required
def confirm_payment(request):
    cinfo=ClinicInfoClass.objects.all()
    reservations = reservationClass.objects.filter(user=request.user, status='cart')
   
    if not reservations.exists():     
        return redirect("/checkoutR/") 

    order=orderClass.objects.filter(user=request.user, status='cart').first()
    sm=0
    if reservations:
        for res in reservations:
            sm += res.appointment.schedule.price
               
    if request.method == "POST":
        tracking_code = request.POST.get('tracking_code')
        payment_receipt = request.FILES.get('payment_receipt')
        if tracking_code and payment_receipt:
            for reservation in reservations:
                reservation.payment_tracking_code = tracking_code
                reservation.payment_receipt = payment_receipt
                reservation.status = 'pending'
                reservation.save()
            return redirect("/invoice/") 

    return render(request, "main_app/confirmPayment.html", context={"reservation": reservations,"cinfo":cinfo,"order":order,"sm":sm})


@login_required
def invoice(request):
    cinfo = ClinicInfoClass.objects.all()
    order = orderClass.objects.get(user=request.user)
    reservations = reservationClass.objects.filter(user=request.user, status='pending')

    total_price = sum(res.appointment.schedule.price for res in reservations)

    return render(request, "main_app/invoice.html", {
        "order": order,
        "reservations": reservations,
        "cinfo": cinfo,
        "total_price": total_price
    })



@staff_member_required
def admin_approve_reservation(request, reservation_id):
    reservation = get_object_or_404(reservationClass, id=reservation_id)
    if reservation.status == 'pending':
        reservation.status = 'final'  
        reservation.admin_approval = True  
        reservation.save()

    return redirect("/admin/reservations/")



@login_required
def addreservation(request,adad):
    appointment = get_object_or_404(appointmentClass, id=adad) 
    if reservationClass.objects.filter(appointment=appointment, status='cart').exists():
        return redirect("/reservation/")    

    expiration_time = timezone.now() + timedelta(hours=2)
    reservation = reservationClass.objects.create(
        user=request.user,
        appointment=appointment,
        status="cart",
        expires_at=expiration_time
    )

    appointment.schedule.is_available = False  
    appointment.schedule.save() 

    return redirect("/reservation/")



@login_required
def reservation(request):
    reservations = reservationClass.objects.filter(user=request.user, status='cart')
    
    for reservation in reservations:
        if reservation.expires_at < timezone.now():
            reservation.status = 'expired'  
            reservation.appointment.schedule.is_available = True   
            reservation.appointment.schedule.save()    
            reservation.save()   
            reservation = None  
    
    reservations = reservationClass.objects.filter(user=request.user, status='cart')
    sm = 0 
    if reservations:
        for res in reservations:
            sm += res.appointment.schedule.price
    cinfo=ClinicInfoClass.objects.all() 
    reservation = reservationClass.objects.filter(user=request.user, status='cart')
    order=orderClass.objects.filter(user=request.user, status='cart').first()
    return render(request, "main_app/reservation.html", context={"reservations": reservations, "sm": sm, "order":order,"reservation":reservation,"cinfo":cinfo})




@login_required
def checkoutR(request):
    cinfo=ClinicInfoClass.objects.all()
    reservations = reservationClass.objects.filter(user=request.user, status='cart')
    order=orderClass.objects.filter(user=request.user, status='cart').first()
    sm=0
    if reservations:
        for res in reservations:
            sm += res.appointment.schedule.price
    if (request.method=="POST"):
        reservation_id = request.POST.get('reservation_id')

    return render(request, "main_app/checkoutR.html", context={"reservation": reservations, "sm":sm,"cinfo":cinfo,"order":order})



@login_required
def deletecartR(request,itmid):
    reservation=get_object_or_404(reservationClass,id=itmid,user=request.user,status='cart')
    reservation.delete()
    return redirect("/reservation/")



def therapy(request):
    stc=staticcontentClass.objects.filter(key='therapy')
    stp=staticphotoClass.objects.filter(key='therapy')
    reserved_appointments = reservationClass.objects.filter(status__in=["cart", "pending", "final"]).values_list('appointment_id', flat=True)
    if (request.method=="POST"):
        if not request.user.is_authenticated:
            return redirect('/login/?next=' + request.path)
        f=appointmentForm(request.POST)
        if (f.is_valid): 
            f=f.save()
            return redirect(f"/addreservation/{f.id}/")    
    else:
      f=appointmentForm()
      f.fields["schedule"].queryset = scheduleClass.objects.exclude(
            appointments__id__in=reserved_appointments
        )
      
    if request.user.is_authenticated:
        reservation = reservationClass.objects.filter(user=request.user, status='cart')
        order=orderClass.objects.filter(user=request.user, status='cart').first()
    else:
        reservation = None
        order=None
    cinfo=ClinicInfoClass.objects.all()
    return render(request,'main_app/therapy.html',context={"cnt":stc, "ph":stp ,"f":f,"reservation":reservation,"order":order,"cinfo":cinfo}) 



def psychopathy(request):
    stc=staticcontentClass.objects.filter(key='psycholopathy')
    stp=staticphotoClass.objects.filter(key='psycholopathy')
    if (request.method=="POST"):
        if not request.user.is_authenticated:
            return redirect('/login/?next=' + request.path)
        f=appointmentForm(request.POST)
        if (f.is_valid): 
            f=f.save()
            return redirect(f"/addreservation/{f.id}/")    
    else:
        f=appointmentForm()
        
    cinfo=ClinicInfoClass.objects.all()
    if request.user.is_authenticated:
        reservation = reservationClass.objects.filter(user=request.user, status='cart')
        order=orderClass.objects.filter(user=request.user, status='cart').first()
    else:
        reservation = None
        order=None
    return render(request,'main_app/psychopathy.html',context={"cnt":stc,"ph":stp ,"f":f,"cinfo":cinfo,"reservation":reservation,"order":order})



def test(request):
    stc=staticcontentClass.objects.filter(key='test')
    stp=staticphotoClass.objects.filter(key='test')
    cinfo=ClinicInfoClass.objects.all()
    if request.user.is_authenticated:
        reservation = reservationClass.objects.filter(user=request.user, status='cart')
        order=orderClass.objects.filter(user=request.user, status='cart').first()
    else:
        reservation = None
        order=None
    return render(request,'main_app/test.html',context={"cnt":stc,"ph":stp,"cinfo":cinfo,"reservation":reservation,"order":order})



def workshop(request):
    stc=staticcontentClass.objects.filter(key='workshop')
    stp=staticphotoClass.objects.filter(key='workshop')
    ws=workshopClass.objects.all()
    cws=categorywsClass.objects.all()
    cinfo=ClinicInfoClass.objects.all()
    if request.user.is_authenticated:
        reservation = reservationClass.objects.filter(user=request.user, status='cart')
        order=orderClass.objects.filter(user=request.user, status='cart').first()
    else:
        reservation = None
        order=None
    return render(request,'main_app/workshop.html',context={"cnt":stc,"ph":stp , "w":ws , "cw":cws,"cinfo":cinfo,"reservation":reservation,"order":order})



def categoryw(request,adad):
    stc=staticcontentClass.objects.filter(key='workshop')
    stp=staticphotoClass.objects.filter(key='workshop')
    ws=workshopClass.objects.filter(categoryw_id=adad)
    cws=categorywsClass.objects.all()
    cinfo=ClinicInfoClass.objects.all()
    return render(request,'main_app/workshop.html',context={"cnt":stc,"ph":stp , "w":ws , "cw":cws,"cinfo":cinfo})



@login_required
def addcart(request,adad):
    service=get_object_or_404(serviceClass,id=adad)
    order,created=orderClass.objects.get_or_create(user=request.user,status='cart')
    orderitem,created=orderItemClass.objects.get_or_create(order=order,service=service)
    orderitem.quantity+=1
    orderitem.save()
    return redirect("/cart/")



@login_required
def deletecart(request,itmid):
    orderitem=get_object_or_404(orderItemClass,id=itmid,order__user=request.user,order__status='cart')
    orderitem.delete()
    return redirect("/cart/")



@login_required
def cart(request):
    orders=orderClass.objects.filter(user=request.user,status='cart').first()
    reservations = reservationClass.objects.filter(user=request.user, status='cart')
    sm=0
    quan=0
    for i in orders.items.all():
        first_srv=i.service.srv.first()
        if first_srv:
            sm += first_srv.price * i.quantity
            quan+=i.quantity
    cinfo=ClinicInfoClass.objects.all()
    return render(request,'main_app/cart.html', context={'order':orders,'sm':sm,"cinfo":cinfo,"reservation":reservations,"qaun":quan})



@login_required
def checkout(request):
    orders=orderClass.objects.filter(user=request.user,status='cart').first()
    reservations = reservationClass.objects.filter(user=request.user, status='cart')

    sm=0
    for i in orders.items.all():
        first_srv=i.service.srv.first()
        if first_srv:
            sm += first_srv.price * i.quantity

    cinfo=ClinicInfoClass.objects.all()
    return render(request,'main_app/checkout.html', context={'order':orders,'sm':sm,"cinfo":cinfo,"reservation":reservations})



def team(request):
    stc=staticcontentClass.objects.filter(key='team')
    stp=staticphotoClass.objects.filter(key='team')
    cinfo=ClinicInfoClass.objects.all()
    return render(request,'main_app/team.html',context={"cnt":stc,"ph":stp,"cinfo":cinfo})



def about(request):
    stc=staticcontentClass.objects.filter(key='about')
    stp=staticphotoClass.objects.filter(key='about')
    cinfo=ClinicInfoClass.objects.all()
    return render(request,'main_app/about.html',context={"cnt":stc,"ph":stp,"cinfo":cinfo})



def contact(request):
    cinfo=ClinicInfoClass.objects.all()

    if (request.method=="POST"):
        s=""
        f=contactForm(request.POST)
        if (f.is_valid):
            f.save()
            s=request.POST.get("username")+" "+ "عزیز دیدگاه شما ثبت گردید "
            f=contactForm()
            return render(request,'main_app/contact.html',context={"username":s , "f":f,"cinfo":cinfo})
    else:
      f=contactForm()
      
      return render(request,'main_app/contact.html',context={"f":f,"cinfo":cinfo})



def article(request):
    article=articleClass.objects.all()
    cinfo=ClinicInfoClass.objects.all()
    return render(request,'main_app/article.html',context={"article":article,"cinfo":cinfo})



def gallery(request):
    return render(request,'main_app/gallery.html')



def register(request):
    cinfo=ClinicInfoClass.objects.all()

    if (request.method=="POST"):
        username=request.POST.get("username")
        lname=request.POST.get("lname")
        fname=request.POST.get("fname")
        email=request.POST.get("email")
        passw=request.POST.get("passw")
        customuserClass.objects.create_user(username,email,passw,last_name=lname,first_name=fname,is_staff=False)
        return redirect("/login/")

    return render(request,'main_app/register.html',context={"cinfo":cinfo})



@login_required 
def dashboard(request):
    cinfo=ClinicInfoClass.objects.all()
    if (request.user.rolle=="therapeutist"):
        return render(request,'main_app/dashboard.html',context={"cinfo":cinfo})
    else:
        return redirect("/panel/")



@login_required 
def panel(request):
    cinfo=ClinicInfoClass.objects.all()
    orders=orderClass.objects.filter(user=request.user).first()
    reservations = reservationClass.objects.filter(user=request.user)
    if (request.user.rolle=="client"):
        return render(request,'main_app/userpanel.html',context={"cinfo":cinfo,"orders":orders,"reservations":reservations})
    else:
        return redirect("/dashboard/")



def logout(request):
    cinfo=ClinicInfoClass.objects.all()
    lo(request)
    return redirect('/login')



def login(request):
    if request.user.is_authenticated:
        if request.user.rolle == "therapeutist":
            return redirect("/dashboard/")
        else:
            return redirect("/panel/")
    cinfo=ClinicInfoClass.objects.all()
    if (request.method=="POST"):
        username=request.POST.get("username")
        password=request.POST.get("passw")
        u=authenticate(username=username,password=password)
        if u is not None:
            lg(request,u)
            if  (u.rolle=="therapeutist"):
                return redirect("/dashboard/")
            else:
                return redirect("/panel/")

        else:
                return render(request,'main_app/login.html' ,context={"massage":"نام کاربری یا رمز عبور اشتباه است","cinfo":cinfo})
    else:
        return render(request,'main_app/login.html',context={"cinfo":cinfo})
    
    
    
def popup_login(request):
    if (request.method=="POST"):
        username=request.POST.get("username")
        passw=request.POST.get("passw")
        u=authenticate(username=username,password=passw)
        if u is not None:
            lg(request,u)
            return JsonResponse({'status':'success' , 'message':u.rolle})
        else:
            return JsonResponse({'status':'error' , 'message':"نام کاربری یا رمز عبور اشتباه است"})
                
 

def get_schedule_by_therapist(request):
    therapist_id = request.GET.get("therapist_id")
    
    if therapist_id and scheduleClass.objects.filter(therapeutist_id=therapist_id).exists():
        reserved_schedules = reservationClass.objects.filter(
            status__in=["cart", "pending", "final"]
        ).values_list("appointment__schedule_id", flat=True)

        schedules = scheduleClass.objects.filter(therapeutist_id=therapist_id).exclude(id__in=reserved_schedules)

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






