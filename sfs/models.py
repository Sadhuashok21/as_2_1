""" # This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class AllUsers(models.Model):
    name = models.CharField(max_length=500)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=35)
    user_id = models.CharField(max_length=40, unique=True)
    profile = models.CharField(max_length=2000)
    user_type = models.CharField(max_length=5)
    platform = models.CharField(max_length=10)
    platform_name = models.CharField(max_length=50)
    type = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    ip = models.CharField(max_length=50, default=0)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'all_users'


class Allerrors(models.Model):
    error_id = models.CharField(max_length=300)
    error_msg = models.CharField(max_length=250)
    user_id = models.CharField(max_length=40, default=None)
    ip = models.CharField(max_length=50)
    platform = models.CharField(max_length=10)
    platform_name = models.CharField(max_length=20)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'allerrors'



class BlueCat(models.Model):
    blueprint_category = models.CharField(max_length=20)
    blueprint_name = models.CharField(max_length=35)
    blueprint_img = models.CharField(max_length=30)
    blueprint_para = models.CharField(max_length=400)
    category_id = models.CharField(max_length=25)
    status = models.CharField(max_length=11)
    ip = models.CharField(max_length=50, default=0)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'sfs_bp_cat'


class BpPlaDlv(models.Model):
    ip = models.CharField(max_length=50)
    bp_pla_id = models.CharField(max_length=35)
    download_type = models.CharField(max_length=10)
    user_id = models.CharField(max_length=40, default=0)
    type = models.CharField(max_length=10)
    platform = models.CharField(max_length=10)
    platform_name = models.CharField(max_length=50)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'sfs_bp_dlv'


class Comment(models.Model):
    ip = models.CharField(max_length=50)
    user_id = models.CharField(max_length=40)
    blueprint_id = models.CharField(max_length=40)
    comment = models.CharField(max_length=5000)
    status = models.CharField(max_length=15)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'sfs_comments'

class BP(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    views = models.IntegerField(default=0)
    downloads = models.IntegerField()
    share = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    fviews = models.IntegerField(default=0)
    flikes = models.IntegerField(default=0)
    fdownloads = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    fshare = models.IntegerField(default=0)
    zipfiles = models.CharField(max_length=250)
    sfs_link = models.CharField(max_length=150)
    category = models.CharField(max_length=30)
    preview1 = models.CharField(max_length=40)
    preview2 = models.CharField(max_length=40)
    preview3 = models.CharField(max_length=40)
    type = models.CharField(max_length=20)
    bp_id = models.CharField(max_length=30)
    user = models.ForeignKey(
        AllUsers,
        to_field="user_id",
        db_column = "user_id",
        on_delete=models.CASCADE,
        related_name = "users",
        )
    status = models.CharField(max_length=12)
    ip = models.CharField(max_length=50, default=0)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'sfs_bp'


class TotalActivity(models.Model):
    ip = models.CharField(max_length=50)
    user_id = models.CharField(max_length=40, default=None)
    activity_id = models.CharField(max_length=500)
    platform = models.CharField(max_length=10)
    platform_name = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'total_activity'

 """