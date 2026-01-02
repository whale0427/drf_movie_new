from django.db import models
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import User
from movie.models import Movie

# Create your models here.
class Profile(models.Model):
    uid=ShortUUIDField(verbose_name="用户唯一标识",primary_key=True,unique=True,max_length=32)
    phone=models.CharField(verbose_name="电话",max_length=11,blank=True,null=True,db_index=True)
    email=models.CharField(verbose_name="邮箱",max_length=50,blank=True,null=True,db_index=True)
    avatar=models.CharField(verbose_name="用户头像",max_length=60,blank=True,null=True)
    is_upgrade=models.IntegerField(verbose_name="是否升级会员",default=0)
    upgrade_time=models.DateTimeField(verbose_name="升级日期",blank=True,null=True)
    expire_time=models.DateTimeField(verbose_name="过期时间",blank=True,null=True)
    upgrade_count=models.IntegerField(verbose_name="升级次数",default=0)
    user=models.OneToOneField(User,verbose_name="用户",on_delete=models.CASCADE)
    movie=models.ManyToManyField(Movie,verbose_name="电影")

    def __str__(self):
        return self.user.username

    class Meta:
        db_table="profile"
        verbose_name="用户信息"
        verbose_name_plural="用户信息"