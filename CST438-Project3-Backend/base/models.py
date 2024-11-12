from django.db import models

# Create your models here.

class Lists(models.Model):
    user_id = models.IntegerField()
    list_id = models.AutoField(primary_key=True)
    list_name = models.CharField(max_length=32)
    class Meta:
        db_table = 'lists'

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    signed_in = models.BooleanField(default=False)
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'users'

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    list = models.ForeignKey(Lists, on_delete=models.CASCADE,null=True, blank=True)   # Foreign key to List

    item_name = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)

    item_url = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    quantity = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'items'