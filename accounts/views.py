from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .forms import SignupForm


# def login(request):
#     pass

login = LoginView.as_view(template_name="accounts/login_form.html")

def logout(request):
    messages.success(request, "로그아웃 되었습니다.")
    return logout_then_login(request)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)  # 회원가입과 동시에 로그인 가능
            messages.success(request, '회원가입을 축하드립니다.')
            #signed_user.send_welcome_email() # Celery로 처리 필요
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()

    return render(request, 'accounts/signup_form.html', {'form': form, })