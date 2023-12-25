from django.contrib import admin
from .models import Item, Tax, Discount, Order


class DefaultAdmin(admin.ModelAdmin):
    actions = ['restore_obj', 'delete_from_database']

    @admin.action(description='Restore selected')
    def restore_obj(self, request, queryset):
        for obj in queryset:
            try:
                obj.restore()
            except:
                pass

    @admin.action(description='Erase selected from database')
    def delete_from_database(self, request, queryset):
        for obj in queryset:
            try:
                obj.erase()
            except:
                pass


@admin.register(Item)
class ItemAdmin(DefaultAdmin):
    list_display = ('id', 'name', 'price', 'currency', 'is_delete')
    list_filter = ['is_delete', 'deleted_at', 'currency']
    search_fields = ['id', 'name', 'currency']

    def get_queryset(self, request):
        return Item.all_objects.all()


@admin.register(Tax)
class TaxAdmin(DefaultAdmin):
    list_display = ('id', 'name', 'percentage')
    list_filter = ['is_delete', 'deleted_at']
    search_fields = ['id', 'name', 'percentage']

    def get_queryset(self, request):
        return Tax.all_objects.all()


@admin.register(Discount)
class DiscountAdmin(DefaultAdmin):
    list_display = ('id', 'name', 'percentage', 'more_than_items')
    list_filter = ['is_delete', 'deleted_at']
    search_fields = ['id', 'name', 'percentage']

    def get_queryset(self, request):
        return Discount.all_objects.all()


@admin.register(Order)
class OrderAdmin(DefaultAdmin):
    list_display = ('id', 'currency')
    list_filter = ['is_delete', 'deleted_at']
    search_fields = ['id']

    def get_queryset(self, request):
        return Order.all_objects.all()
