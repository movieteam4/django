from django.db import models

# Create your models here.
class Dreamreal(models.Model):
    website = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=50)
    # online = models.ForeignKey('Online', default=1, on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = "dreamreal"
class createAccount(models.Model):
    mail = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    name=models.CharField(max_length=50,blank=True, null=True)
    # online = models.ForeignKey('Online', default=1, on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = "createAccount"
class verifiedAccount(models.Model):
    mail = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50,blank=True, null=True)  # 姓氏
    date_of_birth = models.DateField( blank=True, null=True)  # 生日
    mobile_phone = models.CharField(max_length=15 , blank=True, null=True)  # 手機
    national_id = models.CharField(max_length=10, blank=True, null=True)  # 身分證字號
    address = models.CharField(max_length=255, blank=True, null=True)  # 地址
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)  # 性別
    education = models.CharField(max_length=100, blank=True, null=True)  # 教育程度
    occupation = models.CharField(max_length=100, blank=True, null=True)  # 職業
    marital_status = models.CharField(max_length=10, choices=[('Single', 'Single'), ('Married', 'Married')], blank=True, null=True)  # 婚姻狀況
    household_income = models.CharField(max_length=50, blank=True, null=True, default="")  # 年收入
    favorite_cinema = models.CharField(max_length=255, blank=True, null=True, default="")  # 最常去的影城
    favorite_genres = models.CharField(max_length=255, blank=True, null=True, default="")  # 喜好電影類型
    preferences = models.CharField(max_length=255, blank=True, null=True, default="")  # 喜好的座位
    score = models.IntegerField(default=0)

    # online = models.ForeignKey('Online', default=1, on_delete=models.CASCADE, db_constraint=False)
    class Meta:
        db_table = "verifiedAccount"
class Favorite(models.Model):
        mail = models.CharField(max_length=50)
        which_movie= models.CharField(max_length=100)
        class Meta:
            db_table = "Favorite"
            unique_together = ('mail', 'which_movie')
class massage(models.Model):
    mail = models.CharField(max_length=50) # 谁收藏
    which_movie = models.CharField(max_length=100)
    what_manage=models.CharField(max_length=300)
    creat_at=models.DateTimeField()
    name= models.CharField(max_length=50,blank=True, null=True)
    title=models.CharField(max_length=50)
    img=models.CharField(max_length=50)
    comment=models.TextField()
    class Meta:
         db_table = "massage"