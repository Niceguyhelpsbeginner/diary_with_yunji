from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from .models import Post, CustomUser
from .forms import PostForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    context = {
        "posts" : posts
    }
    return render(request, 'posts/post_list.html', context= context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('author').order_by('-created_at')
    from .forms import CommentForm
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form
    }
    return render(request, 'posts/post_detail.html', context)

def post_create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():

            new_post = post_form.save()
            return redirect('post-detail', post_id=new_post.id)
    else:
        post_form = PostForm()
    
    return render(request, 'posts/post_form.html', {"form" : post_form})

def post_update(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('post-detail', post_id = post.id)
    else:
        post_form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {"form":post_form})

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('post-list')
    else:
        return render(request, 'posts/post_confirm_delete.html', {"post":post})

def index(request):
    return redirect('post-list')

def register(request):
    print("register view called")
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("form is valid")
            user = form.save()
            login(request, user)
            return redirect('post-list')
    form = CustomUserCreationForm()
    return render(request, 'posts/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'posts/login.html'

    def get_success_url(self):
        return self.request.user.is_authenticated and f"/mypage/{self.request.user.id}/" or "/"

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'posts/mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        user_obj = get_object_or_404(CustomUser, id=user_id)
        context['user_obj'] = user_obj
        return context