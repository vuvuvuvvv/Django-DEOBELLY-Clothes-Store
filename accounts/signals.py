
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import User
from django.shortcuts import redirect
from system.function import generate_random_password_and_hash
from django.contrib.auth import login as auth_login

# from system_function.save_avt import save_avt
@receiver(user_signed_up)
def save_user_gmail_picture_url(sender,**kwargs):
    sociallogin = kwargs['sociallogin']
    print('oke')
    print(f'sociallogin: {sociallogin}')
    provider = sociallogin.account.provider
    print(f'provider: {provider}')
    provider_data = sociallogin.account.extra_data
    print(f'data: {provider_data}')
    if provider == 'facebook':
        # user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
        # picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"            
        # email = user_data['email']
        # first_name = user_data['first_name']
        print('oke')
        return redirect('home')

    # print(f'pr_data: {provider_data}\n') #get information of gg login
    # email = kwargs['email']
    email = provider_data['email']
    profile = User.objects.get(email=email)
    username = email.split("@")[0]
    # success, avt_url = save_avt(provider_data['picture'], username,)
    # if success:
    #     profile.avatar = avt_url
    # else:
    profile.avatar = provider_data['picture']
    profile.username = username
    # profile.password = generate_random_password_and_hash()
    profile.save()
    return redirect('validate_infor_user')

