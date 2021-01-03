from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
# tried to understand @login_required decorator

# def user_login(request):
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             form = LoginForm(request.POST)
#             if form.is_valid():
#                 cd = form.cleaned_data
#                 user = authenticate(request, username=cd['username'],
#                                     password=cd['password'])
#                 if user is not None:
#                     if user.is_active:
#                         login(request, user)
#                         return render(request, 'account/dashboard.html', {'section': 'dashboard'})
#                     else:
#                         return HttpResponse('Disabled account/session expired')
#                 else:
#                     return HttpResponse('Invalid login')
#         else:
#             form = LoginForm()
#         return render(request, 'registration/login.html', {'form': form})
#     else:
#         return render(request, 'account/dashboard.html', {'section': 'dashboard'})
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
        else:
            return render(request, 'account/register.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Updated successfully')
        else:
            messages.error(request, 'Error While Updating your profile')
    else:
        try:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
        except ObjectDoesNotExist:
           return Profile.objects.create(user=request.user)



    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
