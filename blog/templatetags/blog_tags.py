# coding:utf-8

from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count


# 此文件的装饰器用于生成一个可以在django模板中使用的模板标签
# 如果用传给render函数的context参数的方法也可以，但是会产生重复页面，即需要在每个视图中渲染
# 所以采用自定义模板标签的方法，使其在模板中也可以使用“函数”

register = template.Library()


@register.simple_tag()
def get_recent_posts(num=5):
    return Post.objects.all()[:num]


@register.simple_tag()
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag()
def categories():
    # Count计算分类下的文章数，annotate此方法未理解透彻，待解决
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag()
def tags():
    # Count计算分类下的文章数，annotate此方法未理解透彻，待解决
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)