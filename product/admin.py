from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Item, Tax, Discount, Order


class ItemAdminForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'})
        }


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
    list_display = ('image_tag', 'id', 'name', 'price', 'currency', 'is_delete')
    list_filter = ['is_delete', 'deleted_at', 'currency']
    search_fields = ['id', 'name', 'currency']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="auto" />'.format(obj.image.url))
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

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
    list_display = ('id', 'get_total_amount', 'currency', 'is_paid', 'is_delete')
    list_filter = ['is_delete', 'deleted_at']
    search_fields = ['id']
    filter_horizontal = ('items',)

    def get_queryset(self, request):
        return Order.all_objects.all()
