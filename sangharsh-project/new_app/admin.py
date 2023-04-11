from django.contrib import admin

from new_app.models import BloodDonate, Contact, CustomUser, Activity, FoundationAccountSetting
 
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Contact)
admin.site.register(BloodDonate)
admin.site.register(Activity)
admin.site.register(FoundationAccountSetting)
