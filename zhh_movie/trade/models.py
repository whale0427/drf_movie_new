from django.db import models
from account.models import Profile

# Create your models here.
class Card(models.Model):
    card_name=models.CharField(verbose_name="会员卡名称",max_length=100,unique=True)
    #max_digits最大位数，decimal_places小数点后几位，示例：12345678.90 是10位（8位整数 + 2位小数）
    card_price=models.DecimalField(verbose_name="价格",max_digits=10,decimal_places=2)
    duration=models.IntegerField(verbose_name="有效天数")
    info=models.CharField("会员卡简介",max_length=200,blank=True,null=True)
    created_at=models.DateTimeField(verbose_name="创建时间",auto_now_add=True,editable=True)
    update_at=models.DateTimeField(verbose_name="更新时间",auto_now=True,editable=True)

    def __str__(self):
        return self.card_name

    class Meta:
        db_table="card"
        verbose_name="会员信息"
        verbose_name_plural="会员信息"
        ordering=['pk']

class Order(models.Model):
    ORDER_STATUS_CHOICES=(
        ("TRADE_SUCCESS","支付成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("PAYING", "待支付"),
    )
    PAY_TYPE_CHOICES=(
        ("alipay","支付宝"),
        ("wechat","微信"),
    )
    #to_field 是 Django 模型中 ForeignKey 字段的一个参数，指定被关联模型（Profile）中用作关联的字段，而不是默认的主键（id）
    #related_name反向关联命名
    profile=models.ForeignKey(Profile,related_name="orders",to_field="uid",on_delete=models.CASCADE,verbose_name="用户信息")
    #related_name="+"禁止反向关联，on_delete=models.DO_NOTHING禁止联级删除，意思是禁止card表删除之后，order会被删除。上面的就是profile被删除，那么order就被删除
    card=models.ForeignKey(Card,related_name="+",on_delete=models.DO_NOTHING,verbose_name="会员卡")
    order_sn=models.CharField(verbose_name="订单编号",max_length=30,blank=True,null=True,unique=True)
    trade_no=models.CharField(verbose_name="交易号",max_length=100,blank=True,null=True,unique=True)
    pay_status=models.CharField(verbose_name="订单状态",choices=ORDER_STATUS_CHOICES,max_length=30,default="PAYING")
    pay_type=models.CharField(verbose_name="支付类型",choices=PAY_TYPE_CHOICES,max_length=10,default="alipay")
    order_mount=models.DecimalField(verbose_name="订单金额",max_digits=10,decimal_places=2)
    pay_time=models.DateTimeField(verbose_name="支付时间",blank=True,null=True)
    created_at=models.DateTimeField(verbose_name="创建时间",auto_now_add=True,editable=True)
    updated_at=models.DateTimeField(verbose_name="更新时间",auto_now=True,editable=True)

    def __str__(self):
        return str(self.order_sn)

    class Meta:
        db_table="order"
        verbose_name="订单信息"
        verbose_name_plural="订单信息"