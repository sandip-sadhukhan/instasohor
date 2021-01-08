from django.shortcuts import render, redirect, HttpResponse
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decorators import unauthentiated_user
from .models import Profile, Post, UserFollowing, Comment
from django.core.paginator import Paginator

# Home page i.e instasohor feed
# here will show only ur and ur's following's post order by date
@login_required
def feed(request):
    posts = []
    following = [x.following_user_id for x in request.user.following.all()]
    # print(following)
    for post in Post.objects.filter(user__in=following).order_by('-date'):
        posts.append(post)
    for post in Post.objects.filter(user=request.user).order_by('-date'):
        posts.append(post)

    # Paginatior
    p = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)

    context = {'posts': page, 'noOfPages': p.num_pages}
    # print(posts)

    return render(request, 'social/index.html', context)


# Post a image + caption
@login_required
def addPost(request):
    user = request.user

    if request.method == 'POST' and request.FILES.get('image') != None:
        caption = request.POST.get('caption', '')
        Post.objects.create(user=user, caption=caption, image=request.FILES.get('image'))
        return redirect('feed')
    return render(request, 'social/addPost.html')


# A single post that will show all comments/likes
def post(request, id):
    return render(request, 'social/post.html')

# A user profile page
def user(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except:
        return HttpResponse("404 Not found!")

    # if user and user's profile is exists
    n_following = len(user.following.all())
    n_followers = len(user.followers.all())
    context = {'curr_user': user, 'profile': profile, 'n_following':n_following, 'n_followers':n_followers}
    return render(request, 'social/profile.html', context)

# your profile that will simply redirect you
# in your profile page
def profile(request):
    user = request.user    
    return redirect(f'/u/{user.username}')

# you can change your profile pic and bio
@login_required
def editProfile(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        about = request.POST.get('bio', '')
        profile.about = about
        if(request.FILES.get('image') != None):
            profile.profile_pic = request.FILES.get('image')
            print('yes')
        profile.save()
        return redirect(f'/u/{user.username}')
    context = {'profile': profile}
    return render(request, 'social/editProfile.html', context)

# register as a new user
@unauthentiated_user
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('editProfile')

    form = CreateUserForm()
    context = {'registerForm': form}
    return render(request, 'registration/signup.html', context)

# search functionality based on first name, last name, username
def search(request):
    context= {}
    query = request.GET.get('q', '').strip()
    if query != '':
        # search
        results = []
        
        r1 = User.objects.filter(first_name__contains=query)
        r2 = User.objects.filter(last_name__contains=query)
        r3 = User.objects.filter(username__contains=query)
        for i in r1:
            if i not in results:
                results.append(i)
        for i in r2:
            if i not in results:
                results.append(i)
        for i in r3:
            if i not in results:
                results.append(i)
        context = {'query':query, 'results': results}
    
    return render(request, 'social/search.html', context)


# show followers
def followers(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except:
        return HttpResponse("404 Not found!")
    # users followers
    followers = user.followers.all()
    context = {'title': 'Followers', 'results': followers}
    return render(request, 'social/followers.html', context)

# show Following 
def following(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except:
        return HttpResponse("404 Not found!")
    # users followers
    following = user.following.all()
    context = {'title': 'Following', 'results': following}
    return render(request, 'social/following.html', context)


# toogle following /toggle-follow/username
# current user will follow/toggle follow the another user
@login_required
def toggleFollow(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except:
        return HttpResponse("404 Not found!")
    
    # if two person are same then break
    if(request.user == user):
        return redirect('profile')

    # check if relationship already build
    try:
        exists = UserFollowing.objects.get(user_id=request.user, following_user_id=user)
        exists.delete()
    except:
        # build relationship
        UserFollowing.objects.create(user_id=request.user, following_user_id=user)

    return redirect('profile')
    

# single post
def singlePost(request, id):
    try:
        post = Post.objects.get(id=id)
    except:
        return HttpResponse("404 Not found!")

    context = {'post': post}
    return render(request, 'social/post.html', context)

# comment
@login_required
def comment(request, postId):
    try:
        post = Post.objects.get(id=postId)
    except:
        return HttpResponse("404 Not found!")

    if request.method != "POST":
        return HttpResponse("Only POST request Allowed!")
    
    # post request
    comment_body = request.POST.get('comment', '').strip()
    if(comment_body != ''):
        Comment.objects.create(user = request.user, post = post, body=comment_body)
    return redirect('feed')

# like functionality
@login_required
def like(request, postId):
    try:
        post = Post.objects.get(id=postId)
    except:
        return HttpResponse("404 Not found!")
    
    if request.user in post.liked_users.all():
        post.liked_users.remove(request.user)
    else:
        post.liked_users.add(request.user)
        
    return redirect('feed')

    
# delete post
@login_required
def delete(request, postId):
    try:
        Post.objects.get(user = request.user, id=postId).delete()
    except:
        return HttpResponse("404 Not found!")
    return redirect('feed')