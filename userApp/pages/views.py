from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth
from django.http import HttpResponseRedirect


class Index(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard/')

        return render(request, 'pages/index.html')

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard/')

        # Get form values
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You're now logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('index')


class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard/')

        return render(request, 'pages/register.html')

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard/')

        # Get form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if password match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, "That username is taken")
                return redirect('register')
            else:
                # Check email
                if User.objects.filter(email=email).exists():
                    messages.error(request, "That email is being used")
                    return redirect('register')
                else:
                    user = User.objects.create(
                        username=username, email=email)
                    user.set_password(password)
                    user.save()
                    messages.success(request, "You're register and can login")
                    return redirect('index')

        else:
            messages.error(request, "Password don't match")
            return redirect('register')


class Dashboard(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')

        return render(request, 'pages/dashboard.html')

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')

        # Get form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if password:
            checkPassword = check_password(password, request.user.password)
            if not checkPassword:
                messages.error(request, "Your password is not correct")
                return redirect('dashboard')
            else:
                # Check Username and Email
                if not username or not email:
                    messages.error(request, "Username and email is required")
                    return redirect('dashboard')
                else:
                    # Check username
                    if User.objects.filter(username=username).exists() and username != request.user.username:
                        messages.error(request, "That username is taken")
                        return redirect('dashboard')
                    else:
                        # Check email
                        if User.objects.filter(email=email).exists() and email != request.user.email:
                            messages.error(request, "That email is being used")
                            return redirect('dashboard')
                        else:
                            User.objects.filter(username=request.user.username).update(
                                username=username, email=email)
                            messages.success(
                                request, "Your informations has been updated")
                            return redirect('dashboard')

        else:
            messages.error(request, 'Enter your password')
            return redirect('dashboard')
        return redirect('dashboard')


class Logout(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')

        auth.logout(request)
        messages.success(request, "You're now logged out")
        return redirect('index')
