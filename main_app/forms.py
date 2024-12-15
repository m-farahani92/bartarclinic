from django import forms
from .models import *
from jalali_date.widgets import AdminJalaliDateWidget
from jalali_date.fields import JalaliDateField

class contactForm (forms.ModelForm):
    class Meta:
        model=contactClass
        fields=['username','email','title','message']
        widgets={'username':forms.TextInput(attrs={'placeholder':"نام کاربری" , 'class':"form-control border-0 bg-light px-4" , 'style':"height: 55px;"}),
                 'email':forms.EmailInput(attrs={'placeholder':"آدرس ایمیل" , 'class':"form-control border-0 bg-light px-4" , 'style':"height: 55px;"}),
                 'title':forms.TextInput(attrs={'placeholder':"موضوع" , 'class':"form-control border-0 bg-light px-4" , 'style':"height: 55px;"}),
                 'message':forms.Textarea(attrs={'placeholder':"دیدگاه" , 'class':"form-control border-0 bg-light px-4 py-3", 'rows':"5"}),
                 }
              
        
class registerForm (forms.ModelForm):
    class Meta:
        model=registerClass
        fields=['fname','lname','username','email','mobile','address','passw','confirmpassw']
        widgets={'fname':forms.TextInput(attrs={'placeholder':"نام " , 'class':"form-control border-0 bg-light px-4" , 'style':"height: 55px;", 'required':"True"}),
                 'lname':forms.TextInput(attrs={'placeholder':"نام خانوادگی  " , 'class':"form-control border-0 bg-light px-4" , 'style':"height: 55px;", 'required':"True"}),
                 'username':forms.TextInput(attrs={'placeholder':"نام کاربری" , 'class':"form-control border-0 bg-light px-4" , 'style':"height: 55px;", 'required':"True"}),
                 'email':forms.EmailInput(attrs={'placeholder':"آدرس ایمیل" , 'class':"form-control border-0 bg-light px-4" , 'style':"height: 55px;", 'required':"True"}),
                 'mobile':forms.TextInput(attrs={'placeholder':"شماره تلفن همراه" , 'class':"form-control border-0 bg-light px-4" , 'style':"height: 55px;", 'required':"True"}),
                 'address':forms.Textarea(attrs={'placeholder':"نشانی" , 'class':"form-control border-0 bg-light px-4 py-3", 'rows':"5"}),
                 'passw':forms.PasswordInput(attrs={'placeholder':"رمز عبور" , 'class':"form-control border-0 bg-light px-4 py-3", 'rows':"5", 'required':"True"}),
                 'confirmpassw':forms.PasswordInput(attrs={'placeholder':"تکرار رمز عبور" , 'class':"form-control border-0 bg-light px-4 py-3", 'rows':"5", 'required':"True"}), 
                 }



class ScheduleForm(forms.ModelForm):
    date = JalaliDateField(widget=AdminJalaliDateWidget)
    start_time = forms.TimeField( widget=forms.TextInput(attrs={'class': 'flatpickr-input'}),label="زمان شروع")
    end_time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'flatpickr-input'}), label="زمان پایان")

    class Meta:
        model = scheduleClass
        fields = ['therapeutist', 'date', 'start_time', 'end_time']
        
        
        
        
        
        
class appointmentForm(forms.ModelForm):
    class Meta:
        model=appointmentClass
        fields=['category','therapeutist','date','start_time','end_time','username','fullname']
        widgets={'category':forms.Select(attrs={'class':"form-select bg-light border-0",'style':"height: 55px;"}),
                       'therapeutist':forms.Select(attrs={'class':"form-select bg-light border-0",'style':"height: 55px;"}),
                       'date':forms.DateField(),
                       'start_time':forms.TimeField(),
                       'end_time':forms.TimeField(),
                       'username':forms.TextInput(),
                       'fullname':forms.TextInput(),
                 }