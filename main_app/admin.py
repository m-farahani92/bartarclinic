from django.contrib import admin
from .models import *

from .forms import ScheduleForm



admin.site.register(contactClass)
admin.site.register(staticcontentClass)
admin.site.register(staticphotoClass)
admin.site.register(categoryClass)
admin.site.register(serviceClass)
admin.site.register(categorywsClass)
admin.site.register(workshopClass)
admin.site.register(therapeutistClass)
admin.site.register(appointmentClass)
admin.site.register(registerClass)
@admin.register(scheduleClass)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleForm
    
class ScheduleAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ['https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css']
        }
        js = [
            'https://cdn.jsdelivr.net/npm/flatpickr',  
            '/static/main_app/js/flatpickr-init.js'      
        ]

    
