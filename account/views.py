from django.shortcuts import render, get_object_or_404
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.paginator import Paginator


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


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    paginator = Paginator(users,3)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    return render(request, 'account/user/list.html', {'section': 'People',
                                                      'users': users})

@login_required
def user_details(request, username):
    user = get_object_or_404(User, username=username, is_active= True)
    return render(request, 'account/user/details.html', {'section': 'people',
                                                         'user': user})



