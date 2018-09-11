from django.core.cache import cache

from common import rds
from post.models import Post


def page_cache(timeout):
    '''页面缓存'''
    def deco(view_func):
        def wrapper(request):
            key = 'PageCache-%s-%s' % (request.session.session_key, request.get_full_path())
            response = cache.get(key)
            print('get from cache: %s' % response)
            if response is None:
                response = view_func(request)
                print('get from view: %s' % response)
                cache.set(key, response, timeout)
                print('set to cache')
            return response
        return wrapper
    return deco


def read_counter(read_view):
    '''帖子阅读计数装饰器'''
    def wrapper(request):
        response = read_view(request)
        # 状态码为 200 时进行计数
        if response.status_code == 200:
            post_id = int(request.GET.get('post_id'))
            rds.zincrby('ReadRank', post_id)
        return response
    return wrapper


def get_top_n(num):
    '''获取排行前 N 的数据'''
    # ori_data = [
    #     (b'38', 369.0),
    #     (b'37', 216.0),
    #     (b'40', 52.0),
    # ]
    ori_data = rds.zrevrange('ReadRank', 0, num - 1, withscores=True)

    # 数据清洗
    # cleaned = [
    #     [38, 369],
    #     [37, 216],
    #     [40, 52],
    # ]
    cleaned = [[int(post_id), int(count)] for post_id, count in ori_data]

    # 方法一：循环操作数据库，性能差
    # for item in cleaned:
    #     post = Post.objects.get(pk=item[0])
    #     item[0] = post

    # 方法二
    post_id_list = [post_id for post_id, _ in cleaned]  # 取出 post id 列表
    posts = Post.objects.filter(id__in=post_id_list)   # 根据 id 批量获取 post
    posts = sorted(posts, key=lambda post: post_id_list.index(post.id))  # 根据 id 位置排序
    for post, item in zip(posts, cleaned):
        item[0] = post  # 逐个替换 post

    # 方法三
    # post_id_list = [post_id for post_id, _ in cleaned]  # 取出 post id 列表
    # # posts = {
    # #     1: <Post: Post object>,
    # #     4: <Post: Post object>,
    # #     6: <Post: Post object>,
    # # }
    # posts = Post.objects.in_bulk(post_id_list)  # 批量获取 post
    # for item in cleaned:
    #     item[0] = posts[item[0]]

    return cleaned
