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
              


class appointmentForm(forms.ModelForm):
    class Meta:
        model = appointmentClass
        fields = ["service", "therapeutist", "schedule", "fullname"]
        widgets = {
            "service": forms.Select(
                attrs={"class": "form-select bg-light border-0", "style": "height: 55px;"}
            ),
            "therapeutist": forms.Select(
                attrs={"class": "form-select bg-light border-0", "style": "height: 55px;"}
            ),
            "schedule": forms.Select(
                attrs={"class": "form-select bg-light border-0", "style": "height: 55px;"}
            ),
            "fullname": forms.TextInput(
                attrs={"class": "form-control bg-light border-0", "style": "height: 55px;", "placeholder": "نام و نام خانوادگی"}
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = serviceClass.objects.filter(category_id=1)
        self.fields['service'].empty_label ="نوع مشاوره"
        self.fields['therapeutist'].empty_label =" درمانگر"
        self.fields['schedule'].empty_label ="زمان مشاوره "

        
class appointmentForm2(forms.ModelForm):
    class Meta:
        model = appointmentClass
        fields = ["service", "therapeutist", "schedule", "fullname"]
        widgets = {
            "service": forms.Select(
                attrs={"class": "form-select bg-light border-0", "style": "height: 55px;"}
            ),
            "therapeutist": forms.Select(
                attrs={"class": "form-select bg-light border-0", "style": "height: 55px;"}
            ),
            "schedule": forms.Select(
                attrs={"class": "form-select bg-light border-0", "style": "height: 55px;"}
            ),
            "fullname": forms.TextInput(
                attrs={"class": "form-control bg-light border-0", "style": "height: 55px;", "placeholder": "نام و نام خانوادگی"}
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = serviceClass.objects.filter(category_id=2)
        self.fields['service'].empty_label ="نوع اختلال"
        self.fields['therapeutist'].empty_label =" درمانگر"
        self.fields['schedule'].empty_label ="زمان مشاوره "
        
        
        
        
# class ScheduleForm(forms.ModelForm):
#     date = JalaliDateField(widget=AdminJalaliDateWidget)
#     start_time = forms.TimeField( widget=forms.TextInput(attrs={'class': 'flatpickr-input'}),label="زمان شروع")
#     end_time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'flatpickr-input'}), label="زمان پایان")

#     class Meta:
#         model = scheduleClass
#         fields = ['therapeutist', 'date', 'start_time', 'end_time']
        

# class worksgshopForm(forms.ModelForm):
#     startw = JalaliDateField(widget=AdminJalaliDateWidget)
#     class Meta:
#         model =workshopClass
#         fields = ['startw']