from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from user.models import User
from user.forms import RegisterForm
from user.helper import get_access_token
from user.helper import get_wb_user_info
from user.helper import login_required


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()

            # 记录登陆状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            request.session['avatar'] = user.avatar
            return redirect('/user/info/')
        else:
            return render(request, 'register.html', {'error': form.errors})
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        nickname = request.POST.get("nickname")
        password = request.POST.get("password")

        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return render(request, 'login.html',
                          {'error': '用户不存在', 'auth_url': settings.WB_AUTH_URL})

        if check_password(password, user.password):
            # 记录登陆状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            request.session['avatar'] = user.avatar
            return redirect('/user/info/')
        else:
            return render(request, 'login.html',
                          {'error': '用户密码错误', 'auth_url': settings.WB_AUTH_URL})
    else:
        return render(request, 'login.html', {'auth_url': settings.WB_AUTH_URL})


def logout(request):
    request.session.flush()
    return redirect('/user/login/')


@login_required
def user_info(request):
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)
    return render(request, 'user_info.html', {'user': user})


def weibo_callback(request):
    code = request.GET.get('code')

    # 获取 access token
    access_token, uid = get_access_token(code)
    if access_token is not None:
        # 获取微博用户信息
        nickname, plt_icon = get_wb_user_info(access_token, uid)
        if nickname is not None:
            user, created = User.objects.get_or_create(nickname=nickname)
            if created:
                user.plt_icon = plt_icon
                user.save()
            # 记录登陆状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            request.session['avatar'] = user.avatar
            return redirect('/user/info/')
    return render(request, 'login.html',
                  {'error': '微博访问异常', 'auth_url': settings.WB_AUTH_URL})
