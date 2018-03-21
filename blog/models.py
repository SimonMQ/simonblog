from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:categories', kwargs={'pk': self.pk})


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=80)
    excerpt = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    views = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    # reverse 函数反向获取其id
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 定义一个views+1的方法，使其保存到数据库
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 定义一个内部类Meta，来指定Post类的一些属性
    class Meta:
        ordering = ['-created_time']

    # 复写save方法，在save之前自动生成excerpt
    def save(self, *args, **kwargs):
        if not self.excerpt:
            # 实例化一个markdown类，用于把渲染过的文本转换成html文本
            # strip_tags用于去掉html文本中的标签
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:80]
        super(Post, self).save(*args, **kwargs)
