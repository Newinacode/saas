from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login

from django.contrib.auth import get_user_model

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'] or None 
        password = request.POST["password"] or None
        if all([username,password]):
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                print("Login here !")
                return redirect('/')

    return render(request,'auth/login.html',{})




def register_view(request):
    if request.method == 'POST':
        username = request.POST['username'] or None
        password = request.POST['password'] or None
        email = request.POST['email'] or None


        #Django Forms
        # user_exists_qs = User.objects.filter(username__iexact=username).exists()
        # email_exists = User.objects.filter(email__iexact=email).exists()
        try:
            User.objects.create_user(username,email=email,password=password)
        except:
            pass
    return render(request,'auth/register.html',{})
