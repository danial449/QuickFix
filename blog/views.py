from django.shortcuts import render , redirect , get_object_or_404
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request , 'blog/post_list.html' , {'posts': posts})

def post_details(request , pk):
    post = get_object_or_404(Post , pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_details' , pk=post.pk)
    else:
        form=CommentForm()
        
    return render(request , 'blog/post_details.html', {'post':post , 'comments':comments , 'form':form})
@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_details' , pk=post.pk)
    else:
        form=PostForm()
    return render(request , 'blog/new_post.html' , {'form':form})

def post_edit(request , pk):
    post = get_object_or_404(Post , pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST , instance = post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_details' , pk=post.pk)
    else:
         form=PostForm(instance = post)
    return render(request , 'blog/new_post.html' , {'form':form})



