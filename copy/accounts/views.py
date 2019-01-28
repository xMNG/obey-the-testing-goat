from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib import auth, messages
from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)

    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid) + '/'
    )
    message_body = f'Use this link to log in:\n\n{url}'

    send_mail(
        subject='Your login link for Superlists',
        message=message_body,
        from_email='noreply@superlists',
        recipient_list=[email],
    )
    messages.success(
        request=request,
        message="Check your email, we've sent you a link you can use to log in."
    )
    return redirect(to='/')

# def login(request):
#     uid = request.GET.get(key='token')
#     user = auth.authenticate(uid=uid)
#     if user:
#         auth.login(request=request, user=user)
#     return redirect(to='/')


def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    print(user)
    if user:
        auth.login(request, user)
    return redirect('/')