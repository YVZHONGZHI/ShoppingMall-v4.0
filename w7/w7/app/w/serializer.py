import re
import uuid

from . import models
from django.db.models import F
from django.contrib import auth
from w7.utils.logger import log
from django.conf import settings
from django.db import transaction
from django.db.models import Count
from rest_framework import serializers
from w7.lib.alipay import alipay, gateway
from django.db.models.functions import TruncMonth
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


# LoginView

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def _get_user_obj(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user_obj = auth.authenticate(username=username, password=password)
        if user_obj:
            return user_obj
        raise ValidationError('用户名或密码错误!')

    def _get_token(self, user_obj):
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, attrs):
        user_obj = self._get_user_obj(attrs)
        token = self._get_token(user_obj)
        self.context['user_obj'] = user_obj
        self.context['token'] = token
        return attrs


# RegisterView

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(min_length=3, max_length=8, allow_blank=True, write_only=True, error_messages={'min_length': '确认密码最少3位!', 'max_length': '确认密码最大8位!'})
    email = serializers.EmailField(allow_blank=True, error_messages={'invalid': '邮箱格式不正确!'})

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'confirm_password', 'email', 'avatar']
        extra_kwargs = {
            'username':{
                'min_length':3, 'max_length':8, 'allow_blank':True,
                'error_messages':{
                    'min_length': '用户名最少3位!',
                    'max_length': '用户名最大8位!'
                }
            },
            'password':{
                'min_length':3, 'max_length':8, 'allow_blank':True,
                'error_messages':{
                    'min_length': '密码最少3位!',
                    'max_length': '密码最大8位!'
                }
            }
        }

    def validate_username(self, attr):
        if not attr:
            raise ValidationError('用户名不能为空!')
        return attr

    def validate_password(self, attr):
        if not attr:
            raise ValidationError('密码不能为空!')
        if not re.match('^[0-9]+$', attr):
            raise ValidationError('密码不能为非数字!')
        return attr

    def validate_confirm_password(self, attr):
        if not attr:
            raise ValidationError('确认密码不能为空!')
        return attr

    def validate_email(self, attr):
        if not attr:
            raise ValidationError('邮箱不能为空!')
        return attr

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password == confirm_password:
            attrs.pop('confirm_password')
            return attrs
        raise ValidationError({'confirm_password': '两次输入的密码不一致!'})

    def create(self, validated_data):
        user_obj = models.UserInfo.objects.create_user(**validated_data)
        return user_obj


# HomeCreatedView

class HomeCreatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Goods
        fields = ['id', 'shop_name', 'desc', 'shop_picture', 'create_time', 'up_num', 'comment_num']


# CreatedView

class CreatedTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ['id', 'name']


class CreatedSerializer(serializers.ModelSerializer):
    tags = CreatedTagSerializer(many=True)

    class Meta:
        model = models.Goods
        fields = ['id', 'shop_name', 'shop_price', 'shop_picture', 'up_num', 'down_num', 'tags']


# ExhibitView

class ExhibitSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password']
        extra_kwargs = {
            'password':{'allow_blank':True, 'write_only':True}
        }

    def validate_password(self, attr):
        if not attr:
            raise ValidationError('账号密码不能为空!')
        if not re.match('^[0-9]+$', attr):
            raise ValidationError('密码不能为非数字!')
        return attr

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user_obj = auth.authenticate(username=username, password=password)
        if user_obj:
            return attrs
        raise ValidationError('账号密码错误!')


# FilterCreatedView   SearchView

class FilterCreatedSerializer(serializers.ModelSerializer):
    date_list = serializers.SerializerMethodField()

    class Meta:
        model = models.Goods
        fields = ['id', 'shop_name', 'desc', 'shop_picture', 'create_time', 'up_num', 'comment_num', 'date_list']

    def get_date_list(self, instance):
        return models.Goods.objects.annotate(month=TruncMonth('create_time')).values('month').annotate(count_num=Count('pk')).values_list('month', 'count_num')


# LeftMenuCategoryCreatedView

class LeftMenuCategoryCreatedSerializer(serializers.ModelSerializer):
    count_num = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'count_num']

    def get_count_num(self, instance):
        return instance.goods_set.count()


# LeftMenuTagCreatedView

class LeftMenuTagCreatedSerializer(serializers.ModelSerializer):
    count_num = serializers.SerializerMethodField()

    class Meta:
        model = models.Tag
        fields = ['id', 'name', 'count_num']

    def get_count_num(self, instance):
        return instance.goods_set.count()


# GoodsDetailCreatedView

class GoodsDetailCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    parent = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ['id', 'content', 'content_time', 'username', 'parent']

    def get_parent(self, instance):
        if instance.parent:
            return instance.parent.user.username
        return None


class GoodsDetailCreatedSerializer(serializers.ModelSerializer):
    comment = GoodsDetailCommentSerializer(many=True, source='comment_set')
    date_list = serializers.SerializerMethodField()

    class Meta:
        model = models.Goods
        fields = ['id', 'shop_name', 'shop_price', 'content', 'shop_picture', 'up_num', 'down_num', 'comment', 'date_list']

    def get_date_list(self, instance):
        return models.Goods.objects.annotate(month=TruncMonth('create_time')).values('month').annotate(count_num=Count('pk')).values_list('month', 'count_num')


# SetPasswordView

class SetPasswordSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    old_password = serializers.CharField(allow_blank=True, write_only=True)
    new_password = serializers.CharField(min_length=3, max_length=8, allow_blank=True, write_only=True, error_messages={'min_length': '新密码最少3位!', 'max_length': '新密码最大8位!'})
    confirm_password = serializers.CharField(min_length=3, max_length=8, allow_blank=True, write_only=True, error_messages={'min_length': '确认密码最少3位!', 'max_length': '确认密码最大8位!'})

    class Meta:
        model = models.UserInfo
        fields = ['username', 'old_password', 'new_password', 'confirm_password']

    def validate_old_password(self, attr):
        if not attr:
            raise ValidationError('原密码不能为空!')
        return attr

    def validate_new_password(self, attr):
        if not attr:
            raise ValidationError('新密码不能为空!')
        if not re.match('^[0-9]+$', attr):
            raise ValidationError('新密码不能为非数字!')
        return attr

    def validate_confirm_password(self, attr):
        if not attr:
            raise ValidationError('确认密码不能为空!')
        return attr

    def validate(self, attrs):
        username = attrs.get('username')
        old_password = attrs.get('old_password')
        user_obj = auth.authenticate(username=username, password=old_password)
        if user_obj:
            new_password = attrs.get('new_password')
            confirm_password = attrs.get('confirm_password')
            if new_password == confirm_password:
                if not new_password == old_password:
                    return attrs
                raise ValidationError('新密码不能与原密码重复')
            raise ValidationError('两次密码不一致')
        raise ValidationError('原密码错误')

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')
        instance.set_password(new_password)
        instance.save()
        return instance


# SetAvatarView

class SetAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserInfo
        fields = ['avatar']

    def update(self, instance, validated_data):
        file_obj = validated_data.get('avatar')
        if file_obj:
            instance.avatar = file_obj
        else:
            instance.avatar = 'avatar/w.jpg'
        instance.save()
        return instance


# BackendCreatedView

class BackendShopCarSerializer(serializers.ModelSerializer):
    goods_id = serializers.CharField(source='goods.id')
    shop_name = serializers.CharField(source='goods.shop_name')
    shop_price = serializers.CharField(source='goods.shop_price')

    class Meta:
        model = models.ShopCar
        fields = ['id', 'shop_time', 'goods_id', 'shop_name', 'shop_price']


class BackendOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['out_trade_no', 'trade_no', 'subject', 'total_amount', 'created_time', 'order_status_name']


class BackendCreatedSerializer(serializers.ModelSerializer):
    car_list = BackendShopCarSerializer(many=True, source='shopcar_set')
    order_list = BackendOrderSerializer(many=True, source='order_set')

    class Meta:
        model = models.UserInfo
        fields = ['car_list', 'order_list']


# ShopCarView

class ShopCarSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=True)
    goods_id = serializers.CharField()

    class Meta:
        model = models.ShopCar
        fields = ['username', 'goods_id']

    def validate_username(self, attr):
        if not attr:
            raise ValidationError('<a href="/login">请先登录</a>')
        return attr

    def validate(self, attrs):
        username = attrs.get('username')
        goods_id = attrs.get('goods_id')
        user = models.UserInfo.objects.filter(username=username).first()
        goods_obj = models.Goods.objects.filter(pk=goods_id).first()
        is_click = models.ShopCar.objects.filter(user=user, goods=goods_obj)
        if not is_click:
            attrs['user'] = user
            attrs['goods_obj'] = goods_obj
            return attrs
        raise ValidationError('不能重复点击')

    def create(self, validated_data):
        user = validated_data.get('user')
        goods_obj = validated_data.get('goods_obj')
        user_obj = models.ShopCar.objects.create(user=user, goods=goods_obj)
        return user_obj


# UpOrDownView

class UpOrDownSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=True)
    is_up = serializers.BooleanField()

    class Meta:
        model = models.Goods
        fields = ['username', 'is_up']

    def validate_username(self, attr):
        if not attr:
            raise ValidationError('<a href="/login">请先登录</a>')
        return attr

    def validate(self, attrs):
        username = attrs.get('username')
        user = models.UserInfo.objects.filter(username=username).first()
        is_click = models.UpAndDown.objects.filter(user=user, goods=self.instance)
        if not is_click:
            attrs['user'] = user
            return attrs
        raise ValidationError('不能重复点击')

    def update(self, instance, validated_data):
        user = validated_data.get('user')
        is_up = validated_data.get('is_up')
        if is_up:
            instance.up_num += 1
            self.context['msg'] = '点赞成功'
        else:
            instance.down_num += 1
            self.context['msg'] = '点踩成功'
        models.UpAndDown.objects.create(user=user, goods=instance, is_up=is_up)
        instance.save()
        return instance


# CommentView

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=True)
    goods_id = serializers.CharField()
    parent_id = serializers.CharField(allow_blank=True)

    class Meta:
        model = models.Comment
        fields = ['username', 'goods_id', 'content', 'parent_id']

    def validate(self, attrs):
        username = attrs.get('username')
        if username:
            user = models.UserInfo.objects.filter(username=username).first()
            attrs.pop('username')
            attrs['user'] = user
            return attrs
        raise ValidationError({'comment_error': '<a href="/login">请先登录</a>'})

    def create(self, validated_data):
        goods_id = validated_data.get('goods_id')
        with transaction.atomic():
            models.Goods.objects.filter(pk=goods_id).update(comment_num=F('comment_num') + 1)
            user_obj = models.Comment.objects.create(**validated_data)
        content_time = user_obj.content_time
        self.context['msg'] = content_time.strftime('%Y-%m-%d %H:%M:%S')
        return user_obj


# PayView

class PaySerializer(serializers.ModelSerializer):
    goods = serializers.PrimaryKeyRelatedField(queryset=models.Goods.objects.all(), write_only=True, many=True)

    class Meta:
        model = models.Order
        fields = ['subject', 'total_amount', 'goods']

    def _check_price(self, attrs):
        total_amount = attrs.get('total_amount')
        goods_list = attrs.get('goods')
        total_price = 0
        for goods in goods_list:
            total_price += goods.shop_price
        if total_amount == total_price:
            return total_amount
        raise ValidationError('价格有误')

    def _get_pay_url(self, out_trade_no, total_amount, subject):
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=out_trade_no,
            total_amount=float(total_amount),
            subject=subject,
            return_url=settings.RETURN_URL,
            notify_url=settings.NOTIFY_URL
        )
        pay_url = gateway + '?' + order_string
        return pay_url

    def validate(self, attrs):
        subject = attrs.get('subject')
        total_amount = self._check_price(attrs)
        code = '%s' % uuid.uuid4()
        out_trade_no = code.replace('-', '')
        attrs['out_trade_no'] = out_trade_no
        pay_url = self._get_pay_url(out_trade_no, total_amount, subject)
        self.context['pay_url'] = pay_url
        user = self.context.get('request').user
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        goods_list = validated_data.pop('goods')
        order = models.Order.objects.create(**validated_data)
        for goods in goods_list:
            models.OrderDetail.objects.create(price=goods.shop_price, order=order, goods=goods)
            if models.ShopCar.objects.filter(user=user, goods=goods).exists():
                models.ShopCar.objects.filter(user=user, goods=goods).delete()
        return order


# SuccessView

class SuccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['trade_no', 'pay_time']

    def update(self, instance, validated_data):
        trade_no = validated_data.get('trade_no')
        pay_time = validated_data.get('pay_time')
        instance.trade_no = trade_no
        instance.order_status = 1
        instance.pay_time = pay_time
        log.warning('%s订单支付成功' % instance.out_trade_no)
        instance.save()
        return instance


# CancelView

class CancelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ShopCar
        fields = '__all__'


# VipView

class VipSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserInfo
        fields = ['username']

    def validate(self, attrs):
        if not self.instance.is_staff:
            return attrs
        raise ValidationError('不能重复购买')

    def update(self, instance, validated_data):
        instance.is_staff = True
        instance.save()
        return instance