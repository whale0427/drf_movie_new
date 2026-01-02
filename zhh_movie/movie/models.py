from django.db import models

# Create your models here.
class Category(models.Model):
    category_name=models.CharField("分类名称",max_length=50)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table="category"
        verbose_name="分类"
        verbose_name_plural="分类管理"
        ordering=["id"]

REGION_CHOICES=[
    (1,"中国大陆"),
    (2,"中国香港"),
    (3,"中国台湾"),
    (4,"美国"),
    (5,"日本"),
    (6,"韩国"),
    (7,"法国"),
    (8,"英国"),
    (9,"其他"),
]
HOT_CHOICES=[
    (False,"否"),
    (True,"是"),
]
TOP_CHOICES=[
    (False,"否"),
    (True,"是"),
]
QUALITY_CHOICES=[
    (1,"720P"),
    (2,"1080P"),
    (3,"4K"),
]
SHOW_CHOICES=[
    (False, "否"),
    (True, "是"),
]
FREE_CHOICES=[
    (False, "否"),
    (True, "是"),
]

class Movie(models.Model):
    movie_name=models.CharField(verbose_name="电影名称",max_length=100)
    release_year=models.IntegerField(verbose_name="上映年份")
    release_date=models.DateField(verbose_name="上映日期")
    director=models.CharField(verbose_name="导演",max_length=20)
    scriptwriter=models.CharField(verbose_name="编剧",max_length=20)
    actors=models.CharField(verbose_name="主演",max_length=20)
    region=models.SmallIntegerField(verbose_name="地区",choices=REGION_CHOICES,default=1)
    type=models.CharField(verbose_name="类型",max_length=20)
    language=models.CharField(verbose_name="语言",max_length=20)
    duration=models.CharField(verbose_name="时长(集数)",max_length=20)
    alternate_name=models.CharField(verbose_name="电影英文名",max_length=20)
    image_url=models.CharField(verbose_name="图片链接",max_length=300,null=True,blank=True,default="")
    rate=models.DecimalField(verbose_name="豆瓣评分",max_digits=2,decimal_places=1,blank=True,default=0.0)
    review=models.TextField(verbose_name="简介",max_length=500,blank=True,default="")
    is_hot=models.BooleanField(verbose_name="是否热门",choices=HOT_CHOICES,blank=True,default=False)
    is_top=models.BooleanField(verbose_name="是否置顶",choices=TOP_CHOICES,blank=True,default=False)
    quality=models.SmallIntegerField(verbose_name="清晰度",choices=QUALITY_CHOICES,blank=True,default=1)
    subtitle=models.CharField(verbose_name="字幕",max_length=100,blank=True,default="")
    update_info=models.CharField(verbose_name="更新信息",max_length=100,blank=True,default="")
    update_progress=models.CharField(verbose_name="更新进度",max_length=100,blank=True,default="")
    download_info=models.TextField(verbose_name="网盘信息",max_length=500,null=True,blank=True,default="",help_text="每个网盘信息占一行")
    is_show=models.BooleanField(verbose_name="是否显示",choices=SHOW_CHOICES,blank=True,default=False)
    is_free=models.BooleanField(verbose_name="是否免费",choices=FREE_CHOICES,blank=True,default=False)
    #外键
    category=models.ForeignKey(Category,verbose_name="分类",on_delete=models.CASCADE)

    def __str__(self):
        return self.movie_name

    class Meta:
        db_table="movie"
        verbose_name="电影"
        verbose_name_plural="电影管理"
        ordering=["id"]