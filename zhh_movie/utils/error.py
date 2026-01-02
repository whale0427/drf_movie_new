def response_data(status_code=0,message=None,data={},**kwargs):
    return dict({
        "status_code":status_code,
        "message":message,
        "data":data,
    },**kwargs)

class MovieError:
    MovieNoFound = (10001,"电影信息不存在")

class UserError:
    UserNoFound=(20001,"用户信息不存在")
    CollectMovieFailed=(20002,"收藏电影失败")
    CancelMovieFailed=(20003,"取消电影失败")
    NotCollectMovie=(20004,"未收藏该电影")

class AlipayError:
    CardNoFound=(30001,"会员卡信息不存在，参数错误")
    OrderCreateFailed=(30002,"订单创建失败")
    AlipayPageFailed=(30003,"支付页面获取失败")
    OrderStatusError=(30004,"订单支付状态错误")