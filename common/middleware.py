import time

from django.core.cache import cache
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


def simple_middleware(view):
    def wrapper(request):
        print(111)
        response = view(request)
        print(2222)
        return response
    return wrapper


class BlockSpiderMiddleware(MiddlewareMixin):
    '''
    限制访问频率的中间件: 最高频率为 3 次/秒

        1.  1535500000.00
        ------------------------
        2.  1535500000.01
        3.  1535500000.02
        4.  1535500001.00
        ------------------------
        5.  1535500001.17        now
        ------------------------
        6.  1535500001.99
        7.  1535500002.55
    '''
    def process_request(self, request):
        user_ip = request.META['REMOTE_ADDR']
        request_key = 'Request-%s' % user_ip  # 用户请求时间的 key
        block_key = 'Block-%s' % user_ip      # 被封禁用户的 key

        # 检查用户 IP 是否被封禁
        if cache.get(block_key):
            print('你已被封禁')
            return render(request, 'blockers.html')

        # 取出当前时间，及历史访问时间
        now = time.time()
        request_history = cache.get(request_key, [0] * 3)

        # 检查与最早访问时间的间隔
        if now - request_history.pop(0) >= 1:
            print('更新访问时间')
            request_history.append(now)              # 滚动更新时间
            cache.set(request_key, request_history)  # 将时间存入缓存
            return
        else:
            # 访问超过限制，将用户 IP 加入缓存
            print('访问频率超过限制')
            cache.set(block_key, True, 10)  # 封禁用户 24 小时
            return render(request, 'blockers.html')
