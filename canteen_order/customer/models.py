# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Users(models.Model):
    user_id = models.AutoField(primary_key=True, verbose_name='用户编号')
    user_name = models.CharField(unique=True, max_length=16, verbose_name='用户名')
    user_psw = models.CharField(max_length=256, verbose_name='用户密码')
    user_balance = models.IntegerField(verbose_name='用户余额')
    user_status = models.IntegerField(choices=[(0, '冻结'), (1, '活跃')], default=1, verbose_name='用户状态')

    class Meta:
        ordering = ['user_id']
        db_table = 'users'
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name
