r'''
用户
    \
    多对多
    /
角色
    \
    多对多
    /
权限
'''

from django.db import models


class User(models.Model):
    SEX = (
        ('M', '男性'),
        ('F', '女性'),
        ('S', '保密'),
    )
    nickname = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=128)
    icon = models.ImageField()
    plt_icon = models.CharField(max_length=256, blank=True)  # 第三方平台用户的头像
    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=8, choices=SEX)

    @property
    def avatar(self):
        return self.icon.url if self.icon else self.plt_icon

    def roles(self):
        relations = UserRoleRelation.objects.filter(uid=self.id).only('role_id')  # 取出与user与role的关系
        role_id_list = [r.role_id for r in relations]    # 取出对应的 role id 列表
        return Role.objects.filter(id__in=role_id_list)  # 返回对应的 role

    def has_perm(self, perm_name):
        '''检查用户是否具有某个权限'''
        for role in self.roles():
            for perm in role.permissions():
                if perm.name == perm_name:
                    return True
        return False


class UserRoleRelation(models.Model):
    '''用户-角色 关系表'''
    uid = models.IntegerField()
    role_id = models.IntegerField()

    @classmethod
    def add_relation(cls, uid, role_id):
        cls.objects.create(uid=uid, role_id=role_id)

    @classmethod
    def del_relation(cls, uid, role_id):
        cls.objects.get(uid=uid, role_id=role_id).delete()


class Role(models.Model):
    '''
    角色表

        admin   管理员
        manager 版主
        user    普通用户
    '''
    name = models.CharField(max_length=16, unique=True)

    def permissions(self):
        relations = RolePermRelation.objects.filter(role_id=self.id).only('perm_id')  # 取出与role与perm的关系
        perm_id_list = [r.perm_id for r in relations]          # 取出对应的 perm id 列表
        return Permission.objects.filter(id__in=perm_id_list)  # 返回对应的 perm


class RolePermRelation(models.Model):
    '''角色-权限 关系表'''
    role_id = models.IntegerField()
    perm_id = models.IntegerField()

    @classmethod
    def add_relation(cls, role_id, perm_id):
        cls.objects.create(role_id=role_id, perm_id=perm_id)

    @classmethod
    def del_relation(cls, role_id, perm_id):
        cls.objects.get(role_id=role_id, perm_id=perm_id).delete()


class Permission(models.Model):
    '''
    权限表

        add_post    添加帖子权限
        del_post    删除帖子权限
        add_comment 添加评论权限
        del_comment 删除评论权限
        del_user    删除用户权限
    '''
    name = models.CharField(max_length=16, unique=True)
