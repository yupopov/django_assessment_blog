from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin
import datetime

from .models import Blogger, Post, Comment
from .forms import CommentForm

# Create your views here.


def index(request):
    """
    The view function for generating the blog home page.
    """
    # Counting the number of bloggers, posts and comment posts
    num_bloggers = Blogger.objects.count()
    num_posts = Post.objects.all().count()
    num_comments = Comment.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Rendering the template passing the context variables
    return render(
        request,
        'index.html',
        context={
            'num_bloggers': num_bloggers,
            'num_posts': num_posts,
            'num_comments': num_comments
            },
    )


class PostListView(ListView):
    model = Post
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post


class BloggerListView(ListView):
    model = Blogger
    paginate_by = 5


class BloggerDetailView(DetailView):
    model = Blogger
    paginate_by = 5


class BloggerUpdate(UpdateView, LoginRequiredMixin):
    model = Blogger
    # Add a check "request.user == blogger"
    # permission_required = ('user.is_staff', )
    fields = ['bio']


class BloggerDelete(DeleteView):
    model = Blogger
    # Add a check verifying if the user who wants to delete the account
    # is the blooger himself
    # permission_required = ('user.is_staff', 'catalog.delele_author')
    success_url = reverse_lazy('authors')


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']


class PostUpdate(UpdateView):
    model = Post
    # Add a check "request.user == blogger"
    # permission_required = ('user.is_staff', )
    fields = ['title', 'content']


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    # Add a check "request.user == blogger"
    # permission_required = ('user.is_staff', 'catalog.delele_book')
    success_url = reverse_lazy('blogger-detail')
    # ADD THE BLOGGER pk


def post_with_comment_form(request, pk):
    """
    View function for loading a post with all its comments.
    If the request method is POST, then validate the form
    and show the page again.
    """
    post = get_object_or_404(Post, pk=pk)

    # If this is a POST request, process the Form data
    if request.method == 'POST' and request.user.is_authenticated:

        # Create a form instance and populate it with the request data:
        form = CommentForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required:
            comment = Comment(
                author=request.user.blogger,
                date=datetime.datetime.now(),
                content=form.cleaned_data['content'],
                post=post
                )
            comment.save()

            # redirect to a new URL:
            return HttpResponseRedirect(
                reverse('blog:post-detail', kwargs={'pk': pk})
                )

    # If this is a GET (or any other method) create the default form.
    else:
        form = CommentForm()

    return render(
        request,
        'blog/post_detail.html',
        {'post': post, 'form': form}
        )
