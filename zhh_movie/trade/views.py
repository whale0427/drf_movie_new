from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.conf import settings

from .models import Card,Order
from .serializers import CardSerializer,OrderSerializer
from .permissions import CardPermission
from utils.error import response_data,AlipayError
from utils.alipay import Alipay
from utils.common import random_number
from account.models import Profile

# Create your views here.
class CardViewSet(viewsets.ModelViewSet):
    queryset=Card.objects.all()
    serializer_class=CardSerializer
    permission_classes=[CardPermission]

class AlipayAPIView(APIView):

    def get(self,request,pk):
        try:
            card=Card.objects.get(pk=pk)
        except:
            return Response(response_data(*AlipayError.AlipayError))
        out_trade_no="pay"+datetime.now().strftime("%Y%m%d%H%M%S")+random_number(4)
        total_amount=str(card.card_price)
        subject=card.card_name
        body="支付宝支付，"+card.info
        product_code="FAST_INSTANT_TRADE_PAY"

        order_sn=request.GET.get("order_sn")
        if not order_sn:
            try:
                Order.objects.create(
                    card=card,
                    profile=request.user.profile,
                    order_sn=out_trade_no,
                    order_mount=card.card_price,
                )
            except:
                return Response(response_data(*AlipayError.OrderCreateFailed))
        else:
            try:
                order=Order.objects.get(order_sn=order_sn)
                if order.pay_status != "PAYING":
                    return Response(response_data(*AlipayError.OrderStatusError))
                out_trade_no=order_sn
            except:
                return Response(response_data(*AlipayError.OrderStatusError))

        try:
            alipay = Alipay()
            alipay_url=alipay.trade_page(out_trade_no,total_amount,subject,body,product_code)
            return Response({"alipay_url":alipay_url,"order_sn":out_trade_no})
        except:
            return Response(response_data(*AlipayError.AlipayPageFailed))

    def delete(self, request):
        try:
            order_sn = request.GET.get("order_sn")
        except:
            print("order_sn no found error")
            return Response("订单号不存在")
        try:
            Order.objects.get(order_sn=order_sn).delete()
        except:
            print("order delete error")
            return Response("订单删除失败")
        return Response("删除成功")

class AlipayCallBackAPIView(APIView):

    def post(self,request):
        datas=request.POST.dict()
        sign=datas.pop("sign")
        del datas["sign_type"]
        sorted_list=sorted([(k,v) for k,v in datas.items()])
        unsigned_string="&".join(f"{k}={v}" for k,v in sorted_list)
        alipay=Alipay()
        if not alipay.verify_sign(unsigned_string,sign):
            print("verify sign error")
            return Response("error")
        try:
            order=Order.objects.get(order_sn=datas.get("out_trade_no"))
        except:
            print("order no found error")
            return Response("error")
        if str(order.order_mount)!=datas.get("total_amount"):
            print("order_mount no found error")
            return Response("error")
        if settings.ALIPAY_SELLER_ID!=datas.get("seller_id"):
            print("ALIPAY_SELLER_ID no found error")
            return Response("error")
        if settings.ALIPAY_APP_ID != datas.get("app_id"):
            print("ALIPAY_APP_ID no found error")
            return Response("error")
        if datas.get("trade_status") not in ["TRADE_SUCCESS","TRADE_FINISHED"]:
            print("trade_status no found error")
            return Response("error")
        # try:
        #     with transaction.atomic():
        #         order.trade_no=datas.get("trade_no")
        #         order.pay_status=datas.get("trade_status")
        #         # order.pay_time=datas.get("gmt_payment")
        #         order.pay_time =timezone.now()
        #         order.save()
        #
        #         profile=Profile.objects.get(uid=order.profile.uid)
        #         profile.is_upgrade=1
        #         profile.upgrade_time=timezone.now()
        #         if not profile.expire_time or profile.expire_time<timezone.now():
        #             profile.expire_time=timezone.now()+timedelta(days=order.card.duration)
        #         else:
        #             profile.expire_time+=timedelta(days=order.card.duration)
        #         profile.upgrade_count+=1
        #         profile.save()
        # except Exception as e:
        #     print("事务回滚，原因：",str(e))
        #     try:
        #         order.delete()
        #     except:
        #         print("order delete error")
        #         return Response("error")
        #     print("删除原订单")
        with transaction.atomic():
            order.trade_no=datas.get("trade_no")
            order.pay_status=datas.get("trade_status")
            # order.pay_time=datas.get("gmt_payment")
            order.pay_time =timezone.now()
            order.save()

            profile=Profile.objects.get(uid=order.profile.uid)
            profile.is_upgrade=1
            profile.upgrade_time=timezone.now()
            if not profile.expire_time or profile.expire_time<timezone.now():
                profile.expire_time=timezone.now()+timedelta(days=order.card.duration)
            else:
                profile.expire_time+=timedelta(days=order.card.duration)
            profile.upgrade_count+=1
            profile.save()

        return Response("success")

class OrderFilter(filters.FilterSet):
    order_sn = filters.CharFilter(field_name='order_sn', lookup_expr='icontains')
    trade_no = filters.CharFilter(field_name='trade_no', lookup_expr='icontains')
    class Meta:
        model=Order
        fields=("order_sn","trade_no","pay_status")

class OrderPageSizePagination(PageNumberPagination):
    page_size = 6

class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.all().order_by("-id")
    serializer_class=OrderSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class=OrderFilter
    pagination_class = OrderPageSizePagination
    permission_classes=[IsAdminUser]

    def get_permissions(self):
        if self.request.method in ["PUT","PATCH","DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
