from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm,UpdateUserForm,LichChiTieuForm,NoiDungLichForm,ThuNhapForm,ThongTinChiTieuForm
from .models import User,LichChiTieu,NoiDungLich,ThuNhap,ThongTinChiTieu
from django.contrib import messages  
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Lưu đối tượng người dùng tạm thời, không commit ngay lập tức
            user.set_password(form.cleaned_data['password'])  # Mã hóa mật khẩu
            user.save()  # Lưu đối tượng người dùng sau khi đã mã hóa mật khẩu
            messages.success(request, 'Bạn đã đăng ký thành công. Vui lòng đăng nhập.')
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Đảm bảo tên này khớp với tên được định nghĩa trong urls.py
            else:
                messages.error(request, 'Tài khoản hoặc mật khẩu không chính xác')
        else:
            messages.error(request, 'Thông tin nhập vào form không hợp lệ')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/')
def home_view(request):
    return render(request,'home.html')
from django.http import JsonResponse

@login_required(login_url='/')
def nguoidung_view(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)  # Sử dụng form cập nhật
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Cập nhật thành công'}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = UpdateUserForm(instance=user)
    return render(request, 'NguoiDung.html', {'form': form})
from django.db import IntegrityError

@login_required(login_url='/')
def lich_chi_tieu_view(request):
    if request.method == 'POST':
        form = LichChiTieuForm(request.POST)
        if form.is_valid():
            try:
                lich = form.save(commit=False)
                lich.NguoiDung = request.user
                lich.save()
                messages.success(request, 'Lịch mới đã được thêm thành công.')
                return redirect('lich_chi_tieu')
            except IntegrityError:
                messages.error(request, 'Mã lịch này đã tồn tại cho người dùng của bạn.')
        else:
            messages.error(request, form.errors)
    else:
        form = LichChiTieuForm()
    lichs = LichChiTieu.objects.filter(NguoiDung=request.user)
    return render(request, 'LichChiTieu.html', {'form': form, 'lichs': lichs})
@login_required(login_url='/')
def delete_lich_chi_tieu(request, id):
    LichChiTieu.objects.get(pk=id, NguoiDung=request.user).delete()
    return redirect('lich_chi_tieu')

@login_required(login_url='/')
def noidunglich_view(request, lich_id):
    lich = LichChiTieu.objects.get(pk=lich_id, NguoiDung=request.user)
    noidung_list = NoiDungLich.objects.filter(LichChiTieu=lich).order_by('SoThuTu')
    
    if request.method == 'POST':
        form = NoiDungLichForm(request.POST)
        if form.is_valid():
            noidung = form.save(commit=False)
            noidung.LichChiTieu = lich
            noidung.save()
            return redirect('noidunglich', lich_id=lich_id)
    else:
        form = NoiDungLichForm()
    
    return render(request, 'NoiDungLich.html', {
        'lich': lich,
        'noidung_list': noidung_list,
        'form': form
    })
@login_required(login_url='/')
def delete_noidunglich(request, id):
    noidung = NoiDungLich.objects.get(pk=id, LichChiTieu__NguoiDung=request.user)  # Đảm bảo chỉ người dùng sở hữu mới có thể xóa
    if request.method == 'POST':
        noidung.delete()
        return redirect('noidunglich', lich_id=noidung.LichChiTieu.pk)  # Trở về trang danh sách nội dung lịch
    else:
        return HttpResponse("Không được phép", status=403)
@login_required(login_url='/')
def thunhap_view(request):
    if request.method == 'POST':
        form = ThuNhapForm(request.POST)
        if form.is_valid():
            new_thunhap = form.save(commit=False)
            new_thunhap.user = request.user  
            new_thunhap.save()
            messages.success(request, 'Thu nhập đã được thêm thành công!')
            return redirect('thunhap')
        else:
            messages.error(request, 'Có lỗi khi thêm thu nhập.')
    else:
        form = ThuNhapForm()
    
    # Chỉ lấy thu nhập của người dùng hiện tại
    thunhap_list = ThuNhap.objects.filter(user=request.user)
    return render(request, 'ThuNhap.html', {'form': form, 'thunhap_list': thunhap_list})


@login_required(login_url='/')
def delete_thunhap(request, id):
    thunhap = ThuNhap.objects.get(pk=id)
    thunhap.delete()
    messages.success(request, 'Thu nhập đã được xóa thành công.')
    return redirect('thunhap')

@login_required(login_url='/')
def thongtin_chitieu(request):
    if request.method == 'POST':
        form = ThongTinChiTieuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm thông tin chi tiêu thành công!')
            return redirect('thongtin_chitieu')
        else:
            messages.error(request, 'Thêm thông tin chi tiêu không thành công. Vui lòng kiểm tra lại thông tin!')
    else:
        form = ThongTinChiTieuForm()
    
    thongtin_list = ThongTinChiTieu.objects.all()
    return render(request, 'thongtinchitieu.html', {'form': form, 'thongtin_list': thongtin_list})

@login_required(login_url='/')
def delete_thongtin_chitieu(request, id):
    if request.method == 'POST':
        ThongTinChiTieu.objects.filter(MaTTCT=id).delete()
    return redirect('thongtin_chitieu')