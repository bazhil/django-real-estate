from django.contrib import admin
from .models import Enquiry

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'phone_number', 'message']

admin.site.register(Enquiry, EnquiryAdmin)
