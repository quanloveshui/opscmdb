from django.db import models


# Create your models here.
class Table(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    host = models.GenericIPAddressField(verbose_name='主机地址',unique=True)
    port = models.IntegerField(default=3306, verbose_name='主机端口')

    pro = models.CharField(max_length=64, verbose_name='省份')
    city = models.CharField(max_length=512, verbose_name='地市')

    isp = models.CharField(max_length=32, verbose_name='运营商')
    proxy = models.CharField(max_length=128, verbose_name='代理商')

    notes = models.TextField(null=True, verbose_name='备注')

    def __str__(self):
        return self.host

    class Meta:
        pass



class Info(models.Model):
    ip = models.ForeignKey(Table,to_field="host",verbose_name="主机IP",on_delete=models.CASCADE)
    product = models.CharField(max_length=128,verbose_name='厂家')
    os = models.CharField(max_length=128, verbose_name='操作系统')
    sn = models.CharField(max_length=128, verbose_name='序列号')
    mem = models.CharField(max_length=128, verbose_name='内存')
    cpu = models.CharField(max_length=128, verbose_name='CPU型号')
    hostname = models.CharField(max_length=128, verbose_name='主机名')

    def __str__(self):
        return self.hostname

    class Meta:
        pass