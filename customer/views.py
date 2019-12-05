from django.shortcuts import render
from rest_framework import viewsets

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model

#from customer.models import User
from .api.serializers import CustomerSerializer

# Create your views here.


User = get_user_model()


def register(request):

    if request.method == 'POST':
        if 'customerCreate' in request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if not User.objects.filter(email=email).exists():
                if password1 == password2:
                    '''if User.objects.filter(username=username).exists():
                        messages.info(request, 'Username Taken')
                        return HttpResponseRedirect(reverse('register'))
                    if User.objects.filter(email=email).exists():
                        messages.info(request, 'Email Taken')
                        return HttpResponseRedirect(reverse('signup'))
                    else:'''
                    user = User.objects.create_user(
                        username=email, email=email, password=password1, first_name=first_name, last_name=last_name, is_customer=True)
                    user.save()
                    return HttpResponseRedirect(reverse('customer:user_login'))
                else:
                    messages.info(request, 'Password not matching')
                    return HttpResponseRedirect(reverse('customer:signup'))
            else:
                messages.info(request, 'Email taken')
                return HttpResponseRedirect(reverse('customer:signup'))
            return HttpResponseRedirect(reverse('customer:user_login'))
        elif 'companyCreate' in request.POST:
            first_name = request.POST['company_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if User.objects.filter(first_name=first_name).exists():
                    messages.info(request, 'Name Taken')
                    return HttpResponseRedirect(reverse('customer:signup'))
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return HttpResponseRedirect(reverse('customer:signup'))
                else:
                    user = User.objects.create_user(
                        username=email, email=email, password=password1, first_name=first_name, is_company=True)
                    user.save()
                    return HttpResponseRedirect(reverse('customer:user_login'))
            else:
                messages.info(request, 'Password not matching')
                return HttpResponseRedirect(reverse('customer:signup'))
            return HttpResponseRedirect(reverse('customer:user_login'))

    else:
        return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        print("username="+request.POST['email'] +
              "Pass=" + request.POST['password'])
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/customer/api/')
        else:
            messages.info(request, 'Username or password incorrect')
            return redirect('customer:user_login')
    else:
        return render(request, 'login.html')


def user_logout(request):
    auth.logout(request)
    return redirect(reverse('customer:user_login'))
