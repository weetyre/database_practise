# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import datetime


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, sex, type, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        now = datetime.date.today()
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            sex=sex,
            type=type,
            created_at=now,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, sex, email, type, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            sex=sex,
            type=type,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        max_length=20,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    sex = models.CharField(
        verbose_name='sex',
        max_length=10,
        null=True
    )
    type = models.IntegerField(
        verbose_name='type',
        null=True
    )
    created_at = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'#必须有一个唯一标识--USERNAME_FIELD
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'sex','type']#创建super时所必要得字段

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # set current time to created_date
    def set_created_date(self):
        self.created_at = datetime.date.today()

    class Meta:
        db_table = 'myuser'


class Hoster(models.Model):
    hos_id = models.AutoField(primary_key=True)
    contact = models.BigIntegerField(unique=True, blank=True, null=True)
    bonus = models.BigIntegerField(blank=True, null=True)
    coupon_nam = models.CharField(max_length=8, blank=True, null=True)
    pass_field = models.BigIntegerField(db_column='pass', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    loign_nam = models.CharField(max_length=8, blank=True, null=True)
    hos_name = models.CharField(max_length=8, blank=True, null=True)
    sex = models.CharField(max_length=4, blank=True, null=True)
    in_time = models.DateField(auto_now_add=True,blank=True, null=True)

    class Meta:
        db_table = 'hoster'


class Worker(models.Model):
    w_id = models.AutoField(primary_key=True)
    work_area = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(max_length=4, blank=True, null=True)
    in_date = models.DateField(auto_now_add=True,blank=True, null=True)
    work_time = models.FloatField(blank=True, null=True)
    type = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'worker'


class AInfo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    inf_time = models.DateField(auto_now_add=True,blank=True, null=True)

    class Meta:
        db_table = 'a_info'


class Advice(models.Model):
    advice_id = models.IntegerField(primary_key=True, auto_created=True)
    workid = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=True, null=True)
    hoster = models.ForeignKey(Hoster, on_delete=models.CASCADE, blank=True, null=True)
    content_field = models.CharField(db_column='content_', max_length=200, blank=True, null=True)  # Field renamed because it ended with '_'.
    reco_time = models.DateField(auto_now_add=True,blank=True, null=True)
    state = models.BigIntegerField(blank=True, null=True)
    type_re = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'advice'



class Bill(models.Model):
    b_id = models.AutoField(primary_key=True)
    hoster_id = models.ForeignKey(Hoster,on_delete=models.CASCADE)
    b_name = models.CharField(max_length=20, blank=True, null=True)
    b_amount = models.FloatField(blank=True, null=True)
    b_date = models.DateField(auto_now_add=True,blank=True, null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'bill'


class CheckRe(models.Model):
    che_id = models.AutoField(primary_key=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=True, null=True)
    date_ch = models.DateField(auto_now_add=True,blank=True, null=True)
    worktime = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'check_re'


class Equip(models.Model):
    equ_id = models.AutoField(primary_key=True)
    buy_date = models.DateField(auto_now_add=True,blank=True, null=True)
    loca = models.CharField(max_length=20, blank=True, null=True)
    fix_date = models.DateField(auto_now=True,blank=True, null=True)

    class Meta:
        db_table = 'equip'


class Expense(models.Model):
    exp_id = models.IntegerField(primary_key=True, auto_created=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE,blank=True, null=True)
    duty_id = models.BigIntegerField(unique=True, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'expense'


class Fix(models.Model):
    workid = models.ForeignKey(Worker, on_delete=models.CASCADE, db_column='workid', primary_key=True)
    equ = models.ForeignKey(Equip, on_delete=models.CASCADE)
    date_field = models.DateField(auto_now=True, db_column='date_', blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        db_table = 'fix'
        unique_together = (('workid', 'equ'),)


class House(models.Model):
    ho_id = models.AutoField(primary_key=True)
    area = models.FloatField(blank=True, null=True)
    unit_n = models.BigIntegerField(blank=True, null=True)
    avi = models.BigIntegerField(blank=True, null=True)
    bel_name = models.CharField(max_length=10, blank=True, null=True)
    pub_area = models.FloatField(blank=True, null=True)
    bel_id = models.BigIntegerField(blank=True, null=True)
    flour = models.BigIntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    rent = models.FloatField(blank=True, null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=True, null=True)
    host = models.ForeignKey(Hoster,  on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        db_table = 'house'


class InOut(models.Model):
    log_id = models.AutoField(primary_key=True)
    guest_name = models.CharField(max_length=8, blank=True, null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE,blank=True, null=True)
    indate = models.DateField(auto_now=True, blank=True, null=True)
    outdate = models.DateField(auto_now=True, blank=True, null=True)
    contact = models.BigIntegerField(blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    hoster = models.ForeignKey(Hoster,  on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        db_table = 'in_out'


class Operation(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, primary_key=True)
    log = models.ForeignKey(AInfo, on_delete=models.CASCADE)
    date_field = models.DateField(auto_now=True,db_column='date_', blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        db_table = 'operation'
        unique_together = (('worker', 'log'),)


class ParLot(models.Model):
    par_id = models.BigIntegerField(primary_key=True)
    gar_num = models.BigIntegerField()
    rent = models.FloatField(blank=True, null=True)
    avi = models.BigIntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=True, null=True)
    host = models.ForeignKey(Hoster, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'par_lot'
        unique_together = (('par_id', 'gar_num'),)


class Rule(models.Model):
    crea_id = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=True, null=True)
    change_date = models.DateField(auto_now=True,blank=True, null=True)
    type_field = models.BigIntegerField(db_column='type_', blank=True, null=True)  # Field renamed because it ended with '_'.
    crea_time = models.DateField(auto_now_add=True,blank=True, null=True)
    content_field = models.CharField(db_column='content_', max_length=200, blank=True, null=True)  # Field renamed because it ended with '_'.
    rule_id = models.AutoField(primary_key=True,auto_created=True)

    class Meta:
        db_table = 'rule_'


class Salary(models.Model):
    sa_id = models.BigIntegerField(primary_key=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=True, null=True)
    base_sal = models.FloatField(blank=True, null=True)
    handout_time = models.DateField(blank=True, null=True)
    up_sa = models.FloatField(blank=True, null=True)
    secu_sa = models.FloatField(blank=True, null=True)
    deduct = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'salary'


class Uses(models.Model):
    hoster = models.ForeignKey(Hoster,  on_delete=models.CASCADE,primary_key=True)
    equ = models.ForeignKey(Equip, on_delete=models.CASCADE)
    date_field = models.DateField(auto_now=True,db_column='date_', blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        db_table = 'uses'
        unique_together = (('hoster', 'equ'),)


class Look(models.Model):
    hoster = models.ForeignKey(Hoster, on_delete=models.CASCADE, primary_key=True)
    log = models.ForeignKey(AInfo, on_delete=models.CASCADE)
    date_field = models.DateField(auto_now=True, db_column='date_', blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        db_table = 'look'
        unique_together = (('hoster', 'log'),)