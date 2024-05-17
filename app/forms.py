from django import forms
from .models import User,LichChiTieu,NoiDungLich,ThuNhap,ThongTinChiTieu

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
        
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Giới tính')

    class Meta:
        model = User
        fields = ['username', 'password', 'full_name', 'gender', 'birth_year']
        widgets = {
            'password': forms.PasswordInput(),
        }
class UpdateUserForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Giới tính')

    class Meta:
        model = User
        fields = ['full_name', 'gender', 'birth_year']


class LichChiTieuForm(forms.ModelForm):
    class Meta:
        model = LichChiTieu
        fields = ['TenLich', 'NgayBatDau', 'NgayKetThuc']
class NoiDungLichForm(forms.ModelForm):
    class Meta:
        model = NoiDungLich
        fields = ['TenKhoanChi', 'SoTienChi']
class ThuNhapForm(forms.ModelForm):
    class Meta:
        model = ThuNhap
        fields = ['TenTN', 'SoTien', 'Ngay', 'GhiChu']

class ThongTinChiTieuForm(forms.ModelForm):
    class Meta:
        model = ThongTinChiTieu
        fields = ['Ngay', 'SoTien', 'NoiDung', 'GhiChu']