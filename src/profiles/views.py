from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


User = get_user_model()


@login_required
def profile_list_view(request):
    context = {
        'object_list':User.objects.filter(is_active=True)
    }
    print(context)

    return render(request, 'profiles/list.html', context)


@login_required
def profile_detail_view(request,username=None,*args,**kwargs):
    user = request.user
    user_groups = user.groups.all()

    print(
        user.has_perm("subscriptions.basic"),
        user.has_perm("subscriptions.pro"),
        user.has_perm("subscriptions.advanced"),


    )

    if user_groups.filter(name__contains="basic").exists():
        return HttpResponse("Congrats")


    profile_user_obj = get_object_or_404(User,username=username)
    is_me = user == profile_user_obj

    context = {
        'object':profile_user_obj,
        'instance':profile_user_obj,
        'owner':is_me
    }


    # if is_me:
    #     if is_me.has_perm('')

    return render(request, 'profiles/detail.html', context)
