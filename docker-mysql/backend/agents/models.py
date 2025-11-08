from django.db import models

# Create your models here.
class Agent(models.Model):
    # 因为Django 自动会有一个整数型的 id 主键，所以设置 primary_key=True 来覆盖默认的 id 字段
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    full_description = models.TextField()
    avatar = models.URLField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    downloads = models.IntegerField()
    reviews = models.IntegerField()
    author = models.CharField(max_length=100)
    published_at = models.DateField()

    class Meta:
        managed = False          # 告诉 Django 不要迁移/管理这张表
        db_table = 't_app'  # 数据库中真实的表名

    def __str__(self):
        return self.name