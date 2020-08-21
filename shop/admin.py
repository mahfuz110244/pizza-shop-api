from django.contrib import admin
from .models import Tags, Pizza, Order
from core.service import CachingPaginator


# Register your models here.

class PizzaAdmin(admin.ModelAdmin):
    show_full_result_count = False
    paginator = CachingPaginator

    # fields = ['id', 'name', 'brand', 'price', 'weight', 'availability']

    readonly_fields = ['id']

    list_display = ['id', 'name', 'brand', 'price', 'weight', 'availability']


class TagsAdmin(admin.ModelAdmin):
    show_full_result_count = False
    paginator = CachingPaginator

    fields = ['id', 'name']

    readonly_fields = ['id']

    list_display = ['id', 'name']


class OrderAdmin(admin.ModelAdmin):
    show_full_result_count = False
    paginator = CachingPaginator

    # fields = ['id', 'name', 'brand', 'price', 'weight', 'availability']

    readonly_fields = ['id']

    list_display = ['id', 'pizza', 'customer', 'order_price', 'quantity', 'order_state']

    list_select_related = (
        'pizza', 'customer'
    )


admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Order, OrderAdmin)
