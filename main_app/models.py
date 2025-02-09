from django.db import models
from ckeditor.fields import RichTextField
from django_jalali.db import models as jmodels
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
import uuid

class contactClass (models.Model):
    username=models.CharField(max_length=50,verbose_name="نام کاربری")  
    email=models.EmailField(max_length=50,verbose_name="آدرس ایمیل")
    title=models.CharField(max_length=100,verbose_name="عنوان")
    message=models.TextField(verbose_name="پیام") 
    def __str__(self):
        return self.username
    
    
class staticcontentClass (models.Model):
    key=models.CharField(max_length=15,verbose_name="کلید")
    txt=RichTextField(verbose_name="متن")
    title=models.CharField(max_length=100,null=True,verbose_name="عنوان")
    def __str__(self):
        return self.title


class staticphotoClass (models.Model):
    key=models.CharField(max_length=15,verbose_name="کلید")
    img=models.ImageField(upload_to="photo",verbose_name="تصویر")
    title=models.CharField(max_length=100,null=True,verbose_name="عنوان")
    def __str__(self):
        return self.title


class categoryClass(models.Model):
    title=models.CharField(max_length=30,verbose_name="عنوان")
    def __str__(self):
        return self.title
    
    
class serviceClass(models.Model):
    title=models.CharField(max_length=100,verbose_name="عنوان")
    category=models.ForeignKey(categoryClass,on_delete=models.CASCADE,verbose_name="دسته بندی")
    def __str__(self):
        return self.title    


class categorywsClass(models.Model):
    title=models.CharField(max_length=30,verbose_name="عنوان")
    def __str__(self):
        return self.title


class workshopClass(models.Model):
    service=models.ForeignKey(serviceClass,null=True,on_delete=models.CASCADE,limit_choices_to={'category__title': 'برگزاری کارگاه'},related_name="srv",verbose_name="دسته بندی")
    startw = jmodels.jDateField(verbose_name="تاریخ شروع")    
    price=models.IntegerField(verbose_name="قیمت")
    numbsession=models.CharField(max_length=50,verbose_name="تعداد جلسات")
    numbparticipants=models.CharField(max_length=30,verbose_name="تعداد شرکت کنندگان")
    remainingparticipants=models.PositiveIntegerField(default=0,verbose_name="ظرفیت باقیمانده")
    img=models.ImageField(upload_to="photo", null=True,verbose_name="تصویر")
    categoryw=models.ForeignKey(categorywsClass,null=True,on_delete=models.CASCADE,related_name="cw",verbose_name="طیقه بندی")
    def __str__(self):
        return self.service.title
    
    
class orderClass(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    status_choices=[('cart',"سبد خرید"),('final',"سفارش نهایی")      
    ]  
    status=models.CharField(max_length=20,choices=status_choices,default='cart')  
    tracking_code=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def str(self):
        return f"order{self.tracking_code}-{self.status}"


class orderItemClass(models.Model):
    order=models.ForeignKey(orderClass,on_delete=models.CASCADE,related_name="items")
    service=models.ForeignKey(serviceClass,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)    
    def str(self):
        return self.order.tracking_code
    

class therapeutistClass(models.Model):
    name=models.CharField(max_length=35,verbose_name="نام و نام خانوادگی")
    img=models.ImageField(upload_to="photo",verbose_name="عکس پرسنلی")
    degree=models.CharField(max_length=50,verbose_name="تحصیلات")
    services = models.ManyToManyField(
        "serviceClass", 
        blank=True, 
        related_name="therapists"
        ,verbose_name="خدمات"
    )    
    class Meta:
        verbose_name = "درمانگر"
        verbose_name_plural = "درمانگران"
    def __str__(self):
        return self.name


roleitems=(("therapeutist","درمانگر"),("client","مراجعه کننده"))
class customuserClass(AbstractUser):
    rolle=models.CharField(max_length=20,choices=roleitems,default="client")

  
class scheduleClass(models.Model):
    therapeutist = models.ForeignKey(therapeutistClass, on_delete=models.CASCADE, related_name="schedules", verbose_name="درمانگر")
    date = jmodels.jDateField(verbose_name="تاریخ")    
    start_time = models.TimeField(verbose_name="زمان شروع")
    end_time = models.TimeField(verbose_name="زمان پایان")
    price=models.IntegerField(default='380000',verbose_name="هزینه مشاوره")
    is_available = models.BooleanField(default=True, verbose_name="آیا وقت آزاد است؟")

    class Meta:
        verbose_name = "برنامه زمانبندی "
        verbose_name_plural = " برنامه های زمانبندی "
        
    def __str__(self):
        return f"{self.therapeutist.name} - {self.date} ({self.start_time} تا {self.end_time})"    

   
    
class appointmentClass(models.Model):
    service=models.ForeignKey(serviceClass,on_delete=models.CASCADE, related_name="service",null=True)
    therapeutist=models.ForeignKey(therapeutistClass,on_delete=models.CASCADE, related_name="therapeutist")
    schedule = models.ForeignKey(scheduleClass, on_delete=models.CASCADE, related_name="appointments", null=True)
    fullname=models.CharField(max_length=50)  

        

class reservationClass(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    status_choices=[('cart',"سبد خرید"),('pending', " در انتظار تأیید ادمین"),('final',"سفارش نهایی"),('expired', "منقضی شده")
    ]  
    status=models.CharField(max_length=20,choices=status_choices,default='cart')  
    appointment = models.ForeignKey(appointmentClass, on_delete=models.CASCADE, verbose_name="قرار ملاقات",related_name='ap')
    tracking_code=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now)  
    payment_tracking_code = models.CharField(max_length=100, null=True, blank=True) 
    payment_receipt = models.FileField(upload_to='receipts/', null=True, blank=True)  
    admin_approval = models.BooleanField(default=False) 
    def __str__(self):
        return f"{self.user.username} - {self.appointment.fullname} ({self.status})"
    
    
    
class articleClass (models.Model):
   title=models.CharField(max_length=100,verbose_name="عنوان") 
   authors=models.CharField(max_length=100,verbose_name="نویسندگان") 
   abstract=RichTextField(verbose_name="چکیده")
   file_pdf=models.FileField(upload_to='articles/pdfs/', verbose_name="فایل مقاله (PDF)")
   class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        
   def __str__(self):
        return self.title
    
    

class ClinicInfoClass(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام کلینیک")
    address = models.TextField(verbose_name="آدرس")
    phoneNumber = models.CharField(max_length=20, verbose_name="شماره تلفن ثابت",null=True)
    mobileNumber = models.CharField(max_length=20, verbose_name="شماره موبایل")
    email = models.EmailField(verbose_name="ایمیل", blank=True, null=True)
    logo = models.ImageField(upload_to='clinic/logo/', verbose_name="لوگو", blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="عرض جغرافیایی", blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="طول جغرافیایی", blank=True, null=True)
    instagram = models.URLField(verbose_name="لینک اینستاگرام", blank=True, null=True)
    youtube = models.URLField(verbose_name="لینک یوتیوب", blank=True, null=True)
    linkedin = models.URLField(verbose_name="لینک لینکدین", blank=True, null=True)
    facebook = models.URLField(verbose_name="لینک فیسبوک", blank=True, null=True)
    twitter = models.URLField(verbose_name="لینک توییتر", blank=True, null=True)

    