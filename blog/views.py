from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from comments.forms import CommentForm
import markdown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from markdown.extensions.toc import TocExtension
# from django.utils.text import slugify


# 主页视图，显示分页后的文章列表
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)

    page = request.GET.get('page')
    try:
        post_list = paginator.get_page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {'post_list': post_list})


# 文章详情页
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 阅读量+1
    post.increase_views()

    # 引用markdown渲染文章的body。TocExtension(slugify=slugify)显示的中文是十六进制，未解决
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',

    ])
    post.body = md.convert(post.body)
    post.toc = md.toc

    form = CommentForm()

    comment_list = post.comment_set.all()
    context = {'post': post,
               'form': form,
               'comment_list': comment_list,
               }
    return render(request, 'blog/detail.html', context=context)


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


# 文章归档页和分类页同首页视图相似，并且文章是index筛选后的
# 这时就不需要重新定义一个新的模板，可以把筛选后的文章列表渲染到index.html中
# 此处采用filter方法，给定参数，筛选出对应的文章列表
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 由于此处获取的是category的id，所以需要先定义个变量存储此分类id，获取其名称之后传递给filter函数
def categories(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 标签云
def tags(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag)
    return render(request, 'blog/index.html', context={'post_list': post_list})
