# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from canteen.models import Store
from customer.models import Users
from django.urls import reverse


class Dish(models.Model):
    dish_id = models.AutoField(primary_key=True, verbose_name='菜品编号')
    dish_name = models.CharField(max_length=16, verbose_name='菜品名')
    dish_intro = models.CharField(max_length=128, blank=True, null=True, verbose_name='食材列表')
    dish_price = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='价格')
    store = models.ForeignKey(Store, models.CASCADE, verbose_name='所属商铺')
    dish_sales = models.IntegerField(verbose_name='销量')
    dish_store = models.IntegerField(verbose_name='库存')

    class Meta:
        ordering = ['dish_id']
        db_table = 'dish'
        verbose_name = "菜品信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.dish_name

    def get_order_url(self):
        return reverse("dish:get_order", kwargs={'dish_id': self.dish_id})


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True, verbose_name='订单编号')
    user = models.CharField(max_length=16, verbose_name='用户名')
    store = models.IntegerField(verbose_name='商铺id')
    total = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='总价')
    dish_list = models.CharField(max_length=1024, verbose_name='菜品列表')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='下单时间')
    address = models.CharField(max_length=128, default='荔园9栋', verbose_name='下单地址')
    tel= models.CharField(max_length=11, default='11111111111', verbose_name="顾客电话")
    status = models.IntegerField(choices=[(0, '未接单'), (1, '接单')], default=0, verbose_name='订单状态')

    class Meta:
        ordering = ['order_id']
        db_table = 'orders'
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_id)


class Cmt(models.Model):
    comment_id = models.AutoField(primary_key=True, verbose_name='评价编号')
    order = models.ForeignKey(Orders, models.CASCADE, verbose_name='订单编号')
    comment_content = models.CharField(max_length=512, blank=True, null=True, verbose_name='评价内容')
    comment_level = models.IntegerField(choices=[(1, '一星'), (2, '二星'), (3, '三星'), (4, '四星'), (5, '五星')], default=5, verbose_name='评价星级')
    comment_time = models.DateTimeField(verbose_name='评价时间')

    class Meta:
        ordering = ['comment_id']
        db_table = 'cmt'
        verbose_name = "评价信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.comment_id)
