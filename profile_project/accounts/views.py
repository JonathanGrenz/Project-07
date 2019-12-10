from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
    PasswordChangeForm)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect


from . import models
from . import forms


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return redirect('accounts:profile')
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! Time to create your profile."
            )
            return redirect('accounts:edit')
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile_detail(request):
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    form = forms.ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = forms.ProfileForm(
                data=request.POST,
                instance=request.user.profile,
                files=request.FILES
        )
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    return render(request, 'accounts/edit_profile.html', {'form': form})


# https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html
# this site helped with forming the following code.
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            password = form.cleaned_data['new_password1']
            if request.user.check_password(password):
                messages.error(request,
                "Password must differ from your current password!")
                return HttpResponseRedirect(
                    reverse('accounts:change_password'))
            else:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your new password has been saved.')
                return redirect('/accounts/profile')
        else:
            messages.error(request,
                'Please make sure your password complies with the requirements below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
