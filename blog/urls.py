# coding:utf-8


from django.conf.urls import url
from . import views


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ?P<name>为捕获组，范围是0-9组成的任意一个或多个数字，用于在文章中捕获其id
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.categories, name='categories'),
    url(r'^tags/(?P<pk>[0-9]+)/$', views.tags, name='tag'),
]
