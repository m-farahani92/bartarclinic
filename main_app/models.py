from django.db import models
from ckeditor.fields import RichTextField

class contactClass (models.Model):
    username=models.CharField(max_length=50)  
    email=models.EmailField(max_length=50)
    title=models.CharField(max_length=100)
    message=models.TextField() 
    def __str__(self):
        return self.username
    
    
class staticcontentClass (models.Model):
    key=models.CharField(max_length=15)
    txt=RichTextField()
    title=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.title


class staticphotoClass (models.Model):
    key=models.CharField(max_length=15)
    img=models.ImageField(upload_to="photo")
    title=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.title


class categoryClass(models.Model):
    title=models.CharField(max_length=30)
    def __str__(self):
        return self.title
    
    
class serviceClass(models.Model):
    title=models.CharField(max_length=100)
    category=models.ForeignKey(categoryClass,on_delete=models.CASCADE)
    def __str__(self):
        return self.title    


class categorywsClass(models.Model):
    title=models.CharField(max_length=30)
    def __str__(self):
        return self.title


class workshopClass(models.Model):
    category=models.ForeignKey(categoryClass,null=True,on_delete=models.CASCADE,related_name="c")
    title=models.CharField(max_length=50)
    startw=models.DateField()
    price=models.IntegerField()
    numbsession=models.CharField(max_length=50)
    numbparticipants=models.CharField(max_length=30)
    img=models.ImageField(upload_to="photo", null=True)
    categoryw=models.ForeignKey(categorywsClass,null=True,on_delete=models.CASCADE,related_name="cw")
    def __str__(self):
        return self.title
    

class therapeutistClass(models.Model):
    name=models.CharField(max_length=35)
    img=models.ImageField(upload_to="photo")
    degree=models.CharField(max_length=50)
    services = models.ManyToManyField(
        "serviceClass", 
        blank=True, 
        related_name="therapists"
    )    
    def __str__(self):
        return self.name
    

class registerClass(models.Model):
    fname=models.CharField(max_length=30)
    lname=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    mobile=models.IntegerField(max_length=11)
    address=models.CharField(max_length=250)
    passw=models.CharField(max_length=16)
    confirmpassw=models.CharField(max_length=16)
    def __str__(self):
        return self.ussername
    
    
class scheduleClass(models.Model):
    therapeutist = models.ForeignKey(therapeutistClass, on_delete=models.CASCADE, related_name="schedules", verbose_name="درمانگر")
    date = models.DateField(verbose_name="تاریخ")
    start_time = models.TimeField(verbose_name="زمان شروع")
    end_time = models.TimeField(verbose_name="زمان پایان")
    def __str__(self):
        return f"{self.therapeutist.name} - {self.date} ({self.start_time} تا {self.end_time})"    

   
    
class appointmentClass(models.Model):
    category=models.ForeignKey(categoryClass,on_delete=models.CASCADE, related_name="service",null=True)
    therapeutist=models.ForeignKey(therapeutistClass,on_delete=models.CASCADE, related_name="therapeutist")
    schedule = models.ForeignKey(scheduleClass, on_delete=models.CASCADE, related_name="appointments", null=True)
    date = models.DateField(verbose_name="تاریخ حضور", default=None)
    start_time = models.TimeField(verbose_name="زمان شروع حضور", default=None)
    end_time = models.TimeField(verbose_name="زمان پایان حضور", default=None)
    username=models.CharField(max_length=50)  
    fullname=models.CharField(max_length=50)  
    def save(self, *args, **kwargs):
        if self.schedule:
            self.date = self.schedule.date
            self.start_time = self.schedule.start_time
            self.end_time = self.schedule.end_time
        super().save(*args, **kwargs)