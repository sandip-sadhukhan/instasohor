from django.shortcuts import redirect, HttpResponse

def unauthentiated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('feed')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func