from django.contrib import admin
from .models import Customer
from core.service import CachingPaginator


# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    show_full_result_count = False
    paginator = CachingPaginator

    # fields = ['id', 'username', 'password', 'name', 'email', 'address', 'latitude', 'longitude', 'is_admin',
    # 'is_staff', 'image']

    # readonly_fields = ['id', 'password']
    readonly_fields = ['id']

    list_display = ['id', 'username', 'name', 'email', 'address']


admin.site.register(Customer, CustomerAdmin)
