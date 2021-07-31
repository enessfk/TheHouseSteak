from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from product.models import Category, Product, Images, Comment

class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 4

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field="title"
    list_display = ('tree_actions','indented_title',
                    'related_products_count','related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs=super().get_queryset(request)

        qs=Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True
        )

        qs=Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_count',
            cumulative=False
        )
        return qs

    def related_products_count(self,instance):
        return instance.products_count

    related_products_count.short_description = 'Related Products'

    def related_products_cumulative_count(self,instance):
        return instance.products_cumulative_count

    related_products_count.short_description='Related Products in Tree'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category','price','amount','image_tag','statu']
    list_filter = ['statu','category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','product','image_tag']
    readonly_fields = ('image_tag',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment','product','user','status']
    list_filter = ['status']

admin.site.register(Comment,CommentAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images,ImagesAdmin)


