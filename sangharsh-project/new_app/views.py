import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import  get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from new_app.models import BloodDonate, CustomUser, Activity, FoundationAccountSetting, Contact, District
from .forms import AccountSettingForm, ActivityForm, BloodDonateForm, DistrictForm, NewUserForm, NewUserFormOut, UpdateProfileForm, UpdateUserFormAdmin



# Frontend home page
def index(request):
    context={} 
    
    donates= BloodDonate.objects.all()[:6]
    try:
        setting=FoundationAccountSetting.objects.all().first()
    except:
        setting=None
    context['setting'] = setting
    context['raised_fund'] = 12500
    count=0
    for c in donates:
        
        context['donar_review{}'.format(count+1)] = c.message
        context['donar_review{}_author'.format(count+1)] = c.donator
        count +=1
        if count >5:
            break
        
    return render(request, "index.html",context)


# Dashbord
@login_required
def dashbord(request):
    context={}
    user = request.user
    
    # admin and staff dashbord metarial
    if request.user.admin or request.user.staff:
        blood_donates = BloodDonate.objects.filter(donator=user)
        try:
            context['contacts'] = Contact.objects.all()[:5]
        except:
            context['contacts'] = Contact.objects.all()
        
        try:
            context['blood_donates'] = BloodDonate.objects.all()[:5]
        except:
            context['blood_donates'] = BloodDonate.objects.all()
        context['blood_donate_count'] = blood_donates.count()
         
    
    else: # member dashbord metarial
        blood_donates = BloodDonate.objects.filter(donator=user)
        try:
            context['blood_donates'] = blood_donates[:5]
            context['blood_donate_count'] = blood_donates.count()
        except:
            context['blood_donates'] = blood_donates
            context['blood_donate_count'] = blood_donates.count()
        
    user_created_on = user.created_on
    member_since = user.valid_up_to - user_created_on.date()
    context['member_since'] = member_since
        
    return render(request, "user/dashbord.html", context=context)
    

# Register new user
# @login_required
def register_request(request):

    try:
        if request.user.admin or request.user.staff:
            if request.method == "POST":
                form = NewUserForm(request.POST, request.FILES)
                if form.is_valid():
                    user = form.save()
                    login(request, user)
                    return redirect("view_members")
                else:
                    return render (request=request, template_name="user/register.html", context={"form":form})

            form = NewUserForm()
            return render (request=request, template_name="user/register.html", context={"form":form})
    except:
        pass
    
    if request.method == "POST":
        form = NewUserFormOut(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("view_members")
        else:
            return render (request=request, template_name="user/register.html", context={"form":form})

    form = NewUserFormOut()
    return render (request=request, template_name="user/register.html", context={"form":form})
    

@login_required
def view_members(request):
    return render(request, 'user/view_members.html', {'data':CustomUser.objects.all()})


@login_required
def update_user_admin(request, id):
    if request.user.is_admin or request.user.is_staff:
        instance = get_object_or_404(CustomUser, id=id)
        form = UpdateUserFormAdmin(request.POST or None, request.FILES or None, instance=instance)
        if request.method == "POST":
            if form.is_valid:
                form.save()
                return redirect("view_members")
            else:
                pass
    else:
        return redirect('index')
    return render(request, "user/update.html", {'form':form})
        

def login_request(request):

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        email = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        print(user,email,password)
        if user is not None:
            login(request, user)
            return redirect("dashbord")

        else:        
            return render(request=request, template_name="user/login.html", context={"form":form})
            
    form = AuthenticationForm()
    return render(request=request, template_name="user/login.html", context={"form":form})


@login_required
def logout_request(request):
	logout(request)
	return redirect("index")


def view_card(request,id):
    if request.user.valid_up_to < datetime.date.today():
        print("Please renew yor id...")
        return redirect(dashbord)
    instance = get_object_or_404(CustomUser, id=id)
    return render(request, "id.html", {'data':instance})


@login_required
def delete_user(request, id):
    if request.user.is_staff or request.user.is_admin:
        instance = get_object_or_404(CustomUser, id=id)
        if instance.admin:
            pass
        else:
            instance.delete()
    return redirect("view_members")
    
    
@login_required
def profile(request, id=None):
    if id == None:
        id= request.user.id
    instance = get_object_or_404(CustomUser, id=id)
    form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return redirect('dashbord')
    
    return render(request, 'user/profile.html', {'form':form, 'user': instance})


@csrf_exempt
def ajax_fun(request):
    # static/js/ajax.js
    # onclick #contactSubmmit buttom from index.html
    if request.POST['action']=="contact":
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        mobile_nomber=request.POST['mobile_nomber']
        # print(type(mobile_nomber), mobile_nomber)
        if name!='' or email!='':
            cont = Contact(name=name, email=email, message=message,mobile_nomber=mobile_nomber)
            cont.save()
            return JsonResponse({"status": True})
        else:
            pass
    
    
def add_blood_donate(request):
    if request.user.created_on.date() < datetime.date.today():
        print("Please renew yor id...")
        return redirect(view_blood_donate)
    if request.method == "POST":
        form = BloodDonateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashbord')
    else:
        return render(request, 'blood/register.html', {'form':BloodDonateForm()})
    
    
    
def view_blood_donate(request):
    return render(request, 'blood/view.html', {'data': BloodDonate.objects.all()})


def verify_blood_donator(request, id):
    instance = get_object_or_404(BloodDonate, id=id, verify=False)
    if instance:
        instance.verify=True
        instance.save()
        return redirect('dashbord')

    
def view_contacts(request):
    pass
    return render(request, 'contact_view.html', {'contacts':Contact.objects.all()})
    

@login_required
def add_activity(request):
    form = ActivityForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.added_by = request.user
            form.save()
            return redirect('dashbord')
    return render(request, 'activity/add.html', {'form':form})


def view_activity(request):
    activities = Activity.objects.all()
    return HttpResponse(activities)


def add_district(request):
    form = DistrictForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(view_district)
    return render(request, 'distt/add.html', {'form':form})


def view_district(request):
    instanse = District.objects.all()
    return render(request, 'distt/view.html', {'data':instanse})


@login_required
def add_ac_setting(request):
    form = AccountSettingForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.added_by = request.user
            form.save()
            return redirect(view_ac_setting)
    return render(request, 'activity/add.html', {'form':form})


def view_ac_setting(request):
    settings = FoundationAccountSetting.objects.all()
    return render(request, 'setting/view.html', {'data':settings})

