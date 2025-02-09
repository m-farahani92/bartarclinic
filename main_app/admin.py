from django.contrib import admin
from .models import *
from jalali_date.admin import ModelAdminJalaliMixin




admin.site.register(contactClass)
admin.site.register(staticcontentClass)
admin.site.register(staticphotoClass)
admin.site.register(categoryClass)
admin.site.register(serviceClass)
admin.site.register(categorywsClass)
admin.site.register(therapeutistClass)
admin.site.register(appointmentClass)
admin.site.register(customuserClass)
admin.site.register(orderClass)
admin.site.register(orderItemClass)
admin.site.register(reservationClass)
admin.site.register(articleClass)
admin.site.register(ClinicInfoClass)



# display _Schedule by admin
class ScheduleAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('therapeutist', 'jalali_date', 'start_time', 'end_time')

    def jalali_date(self, obj):
        return obj.date.strftime('%Y/%m/%d')  

    jalali_date.short_description = 'تاریخ (شمسی)'

admin.site.register(scheduleClass, ScheduleAdmin)


# display _date_workshop by admin
class workshopAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('jalali_date','startw')

    def jalali_date(self, obj):
        return obj.startw.strftime('%Y/%m/%d')  

    jalali_date.short_description = 'تاریخ (شمسی)'
admin.site.register(workshopClass,workshopAdmin)

    
