from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    avatar = models.FileField(verbose_name='用户头像', upload_to='avatar/', default='avatar/w.jpg')
    create_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(verbose_name='商品分类', max_length=32)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name='商品标签', max_length=32)

    def __str__(self):
        return self.name


class Goods(models.Model):
    shop_name = models.CharField(verbose_name='商品名称', max_length=64)
    shop_price = models.DecimalField(verbose_name='商品单价', max_digits=7, decimal_places=2)
    desc = models.CharField(verbose_name='商品简介', max_length=255)
    content = models.TextField(verbose_name='商品说明')
    shop_picture = models.FileField(verbose_name='商品图片', upload_to='shop_picture/', default='shop_picture/w.jpeg')
    create_time = models.DateField(verbose_name='出售时间', auto_now_add=True)
    up_num = models.BigIntegerField(verbose_name='点赞数', default=0)
    down_num = models.BigIntegerField(verbose_name='点踩数', default=0)
    comment_num = models.BigIntegerField(verbose_name='评论数', default=0)
    category = models.ForeignKey(to='Category', null=True)
    tags = models.ManyToManyField(to='Tag', through='Goods2Tag', through_fields=('goods', 'tag'))

    def __str__(self):
        return self.shop_name


class Goods2Tag(models.Model):
    tag = models.ForeignKey(to='Tag')
    goods = models.ForeignKey(to='Goods')


class UpAndDown(models.Model):
    is_up = models.BooleanField()
    user = models.ForeignKey(to='UserInfo')
    goods = models.ForeignKey(to='Goods')


class Comment(models.Model):
    content = models.CharField(verbose_name='评论内容', max_length=255)
    content_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    user = models.ForeignKey(to='UserInfo')
    goods = models.ForeignKey(to='Goods')
    parent = models.ForeignKey(to='self', null=True)


class ShopCar(models.Model):
    shop_time = models.DateTimeField(verbose_name='进购物车时间', auto_now_add=True)
    user = models.ForeignKey(to='UserInfo')
    goods = models.ForeignKey(to='Goods')


class Order(models.Model):
    out_trade_no = models.CharField(verbose_name="订单号", max_length=64, unique=True)
    trade_no = models.CharField(verbose_name="流水号", max_length=64, null=True)
    subject = models.CharField(verbose_name="订单标题", max_length=64)
    total_amount = models.DecimalField(verbose_name='订单总价', max_digits=8, decimal_places=2)
    order_status = models.IntegerField(verbose_name='订单状态', choices=((0, '未支付'), (1, '已支付')), default=0)
    pay_time = models.DateTimeField(verbose_name="支付时间", null=True)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    user = models.ForeignKey(to='UserInfo')

    def __str__(self):
        return self.out_trade_no

    def order_status_name(self):
        return self.get_order_status_display()


class OrderDetail(models.Model):
    price = models.DecimalField(verbose_name='商品单价', max_digits=7, decimal_places=2)
    order = models.ForeignKey(to='Order')
    goods = models.ForeignKey(to='Goods')

    def __str__(self):
        return self.price