from . import models
from . import serializer
from w7.utils.response import APIResponse
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateAPIView

# Create your views here.


class LoginView(CreateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.LoginSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            username = ser.context['user_obj'].username
            token = ser.context['token']
            return APIResponse(username=username, token=token)
        return APIResponse(code=0, msg=ser.errors)


class RegisterView(CreateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.RegisterSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return APIResponse(msg="注  册  成  功!")
        return APIResponse(code=0, msg=ser.errors)


class HomeCreatedView(ListAPIView):
    queryset = models.Goods.objects
    serializer_class = serializer.HomeCreatedSerializer


class CreatedView(ListAPIView):
    queryset = models.Goods.objects
    serializer_class = serializer.CreatedSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]


class ExhibitView(CreateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.ExhibitSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            return APIResponse()
        return APIResponse(code=0, msg=ser.errors)


class FilterCreatedView(ListAPIView):
    serializer_class = serializer.FilterCreatedSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = models.Goods.objects
        category = self.request.query_params.get('category_id')
        tag = self.request.query_params.get('tags__id')

        if category:
            self.filter_fields = ['category_id']
        elif tag:
            self.filter_fields = ['tags__id']
        return queryset


class LeftMenuCategoryCreatedView(ListAPIView):
    queryset = models.Category.objects
    serializer_class = serializer.LeftMenuCategoryCreatedSerializer


class LeftMenuTagCreatedView(ListAPIView):
    queryset = models.Tag.objects
    serializer_class = serializer.LeftMenuTagCreatedSerializer


class GoodsDetailCreatedView(RetrieveAPIView):
    queryset = models.Goods.objects
    serializer_class = serializer.GoodsDetailCreatedSerializer


class SearchView(ListAPIView):
    queryset = models.Goods.objects
    serializer_class = serializer.FilterCreatedSerializer
    filter_backends = [SearchFilter]
    search_fields = ['shop_name']


class SetPasswordView(UpdateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.SetPasswordSerializer
    lookup_field = 'username'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        ser = self.get_serializer(instance=instance, data=request.data)
        if ser.is_valid():
            ser.save()
            return APIResponse(msg="修改成功")
        return APIResponse(code=0, msg=ser.errors)


class SetAvatarView(RetrieveUpdateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.SetAvatarSerializer
    lookup_field = 'username'


class BackendCreatedView(RetrieveAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.BackendCreatedSerializer
    lookup_field = 'username'
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]


class ShopCarView(CreateAPIView):
    queryset = models.ShopCar.objects
    serializer_class = serializer.ShopCarSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return APIResponse(msg="加入购物车成功")
        return APIResponse(code=0, msg=ser.errors)


class UpOrDownView(UpdateAPIView):
    queryset = models.Goods.objects
    serializer_class = serializer.UpOrDownSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        ser = self.get_serializer(instance=instance, data=request.data)
        if ser.is_valid():
            ser.save()
            msg = ser.context['msg']
            return APIResponse(msg=msg)
        return APIResponse(code=0, msg=ser.errors)


class CommentView(CreateAPIView):
    queryset = models.Comment.objects
    serializer_class = serializer.CommentSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            msg = ser.context['msg']
            return APIResponse(msg=msg)
        return APIResponse(code=0, msg=ser.errors)


class PayView(CreateAPIView):
    queryset = models.Order.objects
    serializer_class = serializer.PaySerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(context={'request': request}, data=request.data)
        if ser.is_valid():
            ser.save()
            pay_url = ser.context['pay_url']
            return APIResponse(msg=pay_url)
        return APIResponse(code=0, msg=ser.errors)


class SuccessView(UpdateAPIView):
    queryset = models.Order.objects
    serializer_class = serializer.SuccessSerializer
    lookup_field = 'out_trade_no'


class CancelView(DestroyAPIView):
    queryset = models.ShopCar.objects
    serializer_class = serializer.CancelSerializer


class VipView(UpdateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.VipSerializer
    lookup_field = 'username'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        ser = self.get_serializer(instance=instance, data=request.data)
        if ser.is_valid():
            ser.save()
            return APIResponse(msg='支付成功')
        return APIResponse(code=0, msg=ser.errors)