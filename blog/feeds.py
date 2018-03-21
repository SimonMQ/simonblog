# coding:utf-8


from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
    # 显示在聚合器上的标题
    title = "SimonDM Django Blog"
    # 通过聚合器跳转到网站的网址
    link = "/"
    # 显示在聚合器上的描述信息
    description = "SimonDM Django Blog RSS测试"

    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    # 聚合其中显示的内容条目的内容
    def item_description(self, item):
        return item.body
