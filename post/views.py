from math import ceil

from django.shortcuts import render, redirect

from post.models import Post
from post.models import Comment
from post.models import Tag
from post.helper import page_cache
from post.helper import read_counter
from post.helper import get_top_n
from user.helper import login_required
from user.helper import check_perm


@page_cache(300)
def post_list(request):
    page = int(request.GET.get('page', 1))  # 当前页码
    per_page = 10  # 每页显示的文章数
    start = (page - 1) * per_page  # 开始的文章
    end = start + per_page
    posts = Post.objects.all().order_by('-id')[start:end]
    total = Post.objects.count()    # 总文章数
    pages = ceil(total / per_page)  # 总页数
    return render(request, 'post_list.html',
                  {'posts': posts, 'pages': range(pages)})


@login_required
# @check_perm('add_post')
def create_post(request):
    if request.method == 'POST':
        uid = request.session['uid']
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(uid=uid, title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    return render(request, 'create_post.html')


@login_required
def edit_post(request):
    if request.method == 'POST':
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(pk=post_id)
        if request.session['uid'] != post.uid:
            return render(request, 'blockers.html')

        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        str_tags = request.POST.get('tags')
        tag_names = [s.strip()
                     for s in str_tags.title().replace('，', ',').split(',')
                     if s.strip()]
        post.update_tags(tag_names)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = int(request.GET.get('post_id'))
        post = Post.objects.get(pk=post_id)
        if request.session['uid'] != post.uid:
            return render(request, 'blockers.html')
        str_tags = ', '.join([t.name for t in post.tags()])
        return render(request, 'edit_post.html', {'post': post, 'tags': str_tags})


@read_counter
@page_cache(5)
def read_post(request):
    post_id = int(request.GET.get('post_id'))
    post = Post.objects.get(pk=post_id)
    return render(request, 'read_post.html', {'post': post})

@login_required
# @check_perm('del_post')
def delete_post(request):
    post_id = int(request.GET.get('post_id'))
    Post.objects.get(pk=post_id).delete()
    return redirect('/')


def search(request):
    keyword = request.POST.get('keyword')
    posts = Post.objects.filter(content__contains=keyword)
    return render(request, 'search.html', {'posts': posts})


def top10(request):
    # rank_data = [
    #     [<Post(37)>,  100],
    #     [<Post(18)>,   94],
    #     [<Post(22)>,   71],
    # ]
    rank_data = get_top_n(10)
    return render(request, 'top10.html', {'rank_data': rank_data})


@login_required
# @check_perm('add_comment')
def comment(request):
    uid = request.session['uid']
    post_id = request.POST.get('post_id')
    content = request.POST.get('content')
    Comment.objects.create(uid=uid, post_id=post_id, content=content)
    return redirect('/post/read/?post_id=%s' % post_id)


@login_required
# @check_perm('del_comment')
def del_comment(request):
    comment_id = int(request.GET.get('comment_id'))
    Comment.objects.get(id=comment_id).delete()
    post_id = int(request.GET.get('post_id'))
    return redirect('/post/read/?post_id=%s' % post_id)


def tag_filter(request):
    tag_id = int(request.GET.get('tag_id'))
    tag = Tag.objects.get(id=tag_id)
    return render(request, 'tag_filter.html', {'tag': tag})
