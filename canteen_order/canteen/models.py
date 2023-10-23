# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Canteen(models.Model):
    canteen_id = models.AutoField(primary_key=True, verbose_name='食堂编号')
    canteen_name = models.CharField(max_length=16, verbose_name='食堂名')
    canteen_status = models.IntegerField(choices=[(0, '关门'), (1, '开门')], default=1, verbose_name='食堂状态')

    class Meta:
        ordering = ['canteen_id']
        db_table = 'canteen'
        verbose_name = "食堂信息"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.canteen_name


class Store(models.Model):
    store_id = models.AutoField(primary_key=True, verbose_name='商铺编号')
    store_name = models.CharField(max_length=16, verbose_name='商铺名')
    canteen = models.ForeignKey(Canteen, models.CASCADE, verbose_name='所属食堂')

    class Meta:
        ordering = ['store_id']
        db_table = 'store'
        verbose_name = "商铺信息"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.store_name


class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True, verbose_name='商家编号')
    store_id = models.IntegerField(verbose_name='商铺编号')
    vendor_name = models.CharField(max_length=16, verbose_name='商家名')
    vendor_psw = models.CharField(max_length=256, verbose_name='商家密码')
    vendor_status = models.IntegerField(choices=[(0, '离线'), (1, '在线')], default=1, verbose_name='商家状态')

    class Meta:
        ordering = ['vendor_id']
        db_table = 'vendor'
        verbose_name = "商家信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.vendor_name
