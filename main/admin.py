from django.contrib import admin

from .models import ExampleImage, Service, OrderImage, Order

admin.site.register(ExampleImage)
admin.site.register(Service)


class OrderImageInline(admin.TabularInline):
    model = OrderImage
    raw_id_fields = ['order']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'user', 'paid', 'created']
    list_filter = ['user', 'service', 'created', 'updated', 'paid']
    inlines = [OrderImageInline]
