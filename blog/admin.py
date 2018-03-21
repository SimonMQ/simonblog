from django.contrib import admin
from .models import Post, Category, Tag


# 在admin后台管理中添加模型
# 定义一个基于admin.ModelAdmin的类，用于更改显示界面
# list_display是一个tuple
# 可选添加搜索栏，参数为post的一些属性
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_time', 'modified_time', 'category', 'author')
    search_fields = ('title',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
