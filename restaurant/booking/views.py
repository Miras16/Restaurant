from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.shortcuts import redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Count
from .forms import CreateUserForm
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import CreateUserForm
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .forms import CommentForm

# Create your views here.
def index(request):
    # picture = Profile.objects.get(user=request.user)
    name = request.user

    if request.method == "POST":
        email = request.POST["email"]
        booking_date = request.POST["booking_date"]
        booking_time = request.POST["booking_time"]

        book = Booking(name=name, email=email, booking_date=booking_date, booking_time=booking_time)
        book.save()
    dishes=DishMenu.objects.all()
    staff=Staff.objects.all()
    yemekler = Subsection.objects.all()[0:3]
    yemekler2 = Subsection.objects.all()[3:6]
    dict = {'staff': staff,'dishes':dishes,
            'yemek': yemekler,
                 'yemek2': yemekler2
            # 'picture':picture
    }
    return render(request, 'booking/index.html',dict)



def register(request):
    form=CreateUserForm()

    if request.method == "POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():

            user = form.save()
            profile = Profile.objects.create(user=user, image='profile_pics/лб.jpg')
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'booking/register.html', {"form": form })

def user_login(request):
    if request.method == "POST":
       username= request.POST.get('username')
       password =request.POST.get('password')

       user=authenticate(request, username=username, password=password)
       if user is not None:
           login(request, user)
           return redirect('home')
       else:
           messages.info(request, 'Username OR password is incorrect')

    context={}
    return render(request, 'booking/login.html', context)

@login_required(login_url='login')
def logoutUser(request):

    logout(request)
    return redirect('login')

def blog(request):
    posts = Posts.objects.all()
    categ = Category.objects.all().annotate(total_categ=Count('title'))

    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dict = {'page_obj': page_obj,'categ': categ,'posts':posts }

    return render(request, 'booking/blog.html',dict,)

def blog_detail(request, slug):
    posts = Posts.objects.all()
    categ = Category.objects.all().annotate(total_categ=Count('title'))
    created_by = request.user
    post=Posts.objects.get(slug=slug)
    c = Comment.objects.filter(post=post).count()
    dict = {'post': post, 'c': c,'posts':posts, 'categ':categ}
    form=None
    if request.method=='POST':
        created_by = request.user
        post = Posts.objects.get(slug=slug)
        name=request.POST.get('Name')
        email=request.POST.get('Email')
        content=request.POST.get('Comment')
        form=Comment.objects.create(name=name,email=email, content=content,post=post,created_by=request.user)
        form.save()
        comments = Comment.objects.all()
        return redirect('post_detail', slug)
    return render(request, 'booking/blog-detail.html',dict)

@login_required
def profile(request):
    bookings = Booking.objects.filter(name=request.user)
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
      u_form = UserUpdateForm(request.POST, instance=request.user)
      p_form = ProfileUpdateForm(request.POST,
                                 request.FILES,
                                 instance=request.user.profile)
      if u_form.is_valid() and p_form.is_valid():
          u_form.save()
          p_form.save()
          messages.success(request, f'Your account has been updated!')
          return redirect('Profile')

    else:
       u_form = UserUpdateForm(instance=request.user)
       p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'profile': profile,
       'u_form': u_form,
       'p_form': p_form,
        'bookings':bookings
    }

    return render(request, 'booking/profile.html', context)

def addpost(request):
    # author=request.user
    # if request.method == "POST":
    #
    #     photo= request.POST["photo"]
    #     title = request.POST["title"]
    #     slug = request.POST["slug"]
    #     content = request.POST["content"]
    #     print(photo)
    #     form=Posts.objects.create(photo=photo, title=title, slug=slug,content=content, author=author)
    #     form.save()
    #     return  redirect('blog')
    #
    #
    # return render(request, 'booking/add_post.html',)

    if request.method == "POST":
        form = AddPost(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return  redirect('blog')
    else:
        form = AddPost()

    return  render(request, 'booking/add_post.html', {'form': form})
def comment_delete(request, id):
    comment = Comment.objects.get(id=id)
    slug = comment.post.slug
    comment.delete()

    return blog_detail(request, slug)


def search(request):
    searched = request.POST['searched']
    obj = Posts.objects.filter(title__contains=searched)
    return render(request, 'booking/search.html', {'searched': searched, 'obj': obj})

def booking_delete(request, id):
    deleteb= Booking.objects.filter(id=id)
    deleteb.delete()
    return redirect('Profile')



