from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password
from django.conf import settings
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)  # Hash the password here
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(username, password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user


# Custom user model
class User(AbstractBaseUser):
    username = models.CharField(primary_key=True, max_length=100, unique=True)
    full_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    birth_year = models.IntegerField()

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
class LichChiTieu(models.Model):
    MaLich = models.AutoField(primary_key=True)
    TenLich = models.CharField(max_length=100)
    NgayBatDau = models.DateField()
    NgayKetThuc = models.DateField()
    NguoiDung = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lichchitieus')
    class Meta:
        unique_together = ('MaLich', 'NguoiDung')
    def __str__(self):
        return self.TenLich
class NoiDungLich(models.Model):
    SoThuTu = models.AutoField(primary_key=True)
    TenKhoanChi = models.CharField(max_length=100)
    SoTienChi = models.DecimalField(max_digits=10, decimal_places=2)
    LichChiTieu = models.ForeignKey('LichChiTieu', on_delete=models.CASCADE, related_name='noidunglich')
    def __str__(self):
        return f"{self.TenKhoanChi} - {self.SoTienChi}"
class ThuNhap(models.Model):
    MaTN = models.AutoField(primary_key=True)
    TenTN = models.CharField(max_length=100)
    SoTien = models.DecimalField(max_digits=10, decimal_places=2)
    Ngay = models.DateField()
    GhiChu = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.TenTN} - {self.SoTien}"
    
class ThongTinChiTieu(models.Model):
    MaTTCT = models.AutoField(primary_key=True)
    Ngay = models.DateField()
    SoTien = models.DecimalField(max_digits=10, decimal_places=2)
    NoiDung = models.CharField(max_length=100)
    GhiChu = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.MaTTCT}: {self.Ngay} - {self.NoiDung}"