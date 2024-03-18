from django.shortcuts import render , redirect , get_object_or_404
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # pagination of services
    paginator = Paginator(posts , 6)
    page_number = request.GET.get('page')
    postfinal = paginator.get_page(page_number)
    totalpage = postfinal.paginator.num_pages

    context ={
        'posts': postfinal,
        'totalpagelist' : [n+1 for n in range(totalpage)]
    }
    return render(request , 'blog/post_list.html' , context)

def post_details(request , pk):
    post = get_object_or_404(Post , pk=pk)
    recent_post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:10]
    comments = post.comments.all()
    # pagination of services
    paginator = Paginator(comments , 10)
    page_number = request.GET.get('page')
    commentsfinal = paginator.get_page(page_number)
    totalpage = commentsfinal.paginator.num_pages

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Submit Successfully! Thank you for your comment.")
            return redirect('blog:post_details' , pk=post.pk)
    else:
        form=CommentForm()
    context = {
        'post':post , 
        'comments':commentsfinal , 
        'form':form,
        'recent_post':recent_post,
        'totalpagelist' : [n+1 for n in range(totalpage)]
    } 
    return render(request , 'blog/post_details.html', context)