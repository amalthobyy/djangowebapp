from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as litlog
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from.models import userinfo
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    error_message=None
    if request.user.is_authenticated:
        return render(request, 'index.html')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username,password=password)
        if user is not None:
            litlog(request,user)
            return redirect('home')
        else:
            error_message =" invalid username&password"

    return render(request, 'login.html',{'error_message': error_message })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'login.html')

def logouthome(request):
    logout(request)
    return render(request,'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.method == 'POST':
        Username = request.POST['username'].strip()
        Name = request.POST['Name'].strip()
        email = request.POST['email'].strip()
        password =request.POST['password'].strip()
        cpassword =request.POST['cpassword'].strip()
        
        if len(Name)>10:
            messages.error(request,'Name must be under 10 letters ')    
            return render(request,'login.html')

        if User.objects.filter(username=Username).exists():
            messages.error(request,'Username allready exists')
            return render (request,'login.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,'email allready exists')
            return render (request,'login.html')
        
        if  password != cpassword:
            messages.error(request,'password not matching')
            return render (request,'login.html')
        
        myUser = User.objects.create_user(Username,email,password)
        myUser.first_name = Name
        myUser.save()
        
        messages.success(request,'your account has created succesfully')
        
        return redirect('login')

    return render(request, 'login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admindash(request):


    if 'is_authenticated' in request.session:
        searchqury =request.GET.get('search','')
        if searchqury:
            users= User.objects.filter(username__istartswith=searchqury)
        else:
            users = User.objects.all()
        return render(request, 'admin.html',{'users':users,'searchqury':searchqury})
    return render(request,'adminlogin.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):
    if 'is_authenticated' in request.session:
        return redirect('admindash')
    username = 'amal'
    password = 'Admin'
    if request.method == 'POST':
        Aname = request.POST['username']
        Apassword =request.POST['password']
        if username == Aname and password==Apassword:
            request.session['is_authenticated'] = True
            return redirect('admindash')
        else:
            error_message =" invalid username&password"

    return render(request, 'adminlogin.html')






@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cuser(request):
     if request.method == 'POST':
        Username = request.POST['username'].strip()
        Name = request.POST['Name']
        email = request.POST['email'].strip()
        password =request.POST['password'].strip()
        cpassword =request.POST['cpassword'].strip()
        
        if len(Name)>10:
            messages.error(request,'Name must be under 10 letters ')    
            return render(request,'cuser.html')

        if User.objects.filter(username=Username).exists():
            messages.error(request,'Username allready exists')
            return render (request,'cuser.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,'email allready exists')
            return render (request,'cuser.html')
        
        if  password != cpassword:
            messages.error(request,'password not matching')
            return render (request,'cuser.html')
        
        myUser = User.objects.create_user(Username,email,password)
        myUser.first_name = Name
        myUser.save()
        


        messages.success(request,'your account has created succesfully')
        
        return redirect('cuser')

    
     return render(request,'cuser.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def alogout(request):
    if 'is_authenticated' in request.session:
        request.session.flush()
        return redirect('adminlogin')
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_delete(request,pk):
    user=User.objects.get(id=pk)
    user.delete()
    user = User.objects.all()
    return render(request, 'admin.html',{'users':user})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_edit(request,user_id):
    if 'is_authenticated' in request.session:
         
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('admin')

        if request.method == 'POST':
            Username = request.POST['username']
            Name = request.POST['name']
            Email = request.POST['email']

            if User.objects.filter(username=Username).exclude(id=user_id).exists():
                messages.error(request, 'Username already exists')
                return redirect('edit',user_id=user.id)
            
            if User.objects.filter(first_name=Name).exclude(id=user_id):
                messages.error(request, 'Username already exists')
                return redirect('edit',user_id=user.id)

            if User.objects.filter(email=Email).exclude(id=user_id).exists():
                messages.error(request, 'Email already exists')
                return redirect('edit',user_id=user.id)

            user.username = Username
            user.first_name = Name
            user.email = Email
            user.save()

            messages.success(request, 'User updated successfully')
            return redirect('admindash')
                
        return render(request, 'edit.html', {'user': user})
    
    else:
        return render(request, 'adminlogin.html')
