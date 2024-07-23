from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin # this is used to make sure that only
                                                          # logged in users can create a post
from django.contrib.auth.mixins import UserPassesTestMixin # this is used to make sure that only
                                                           # the author of the post can update or delete
from django.shortcuts import get_object_or_404  # this is used to get the user object or return 404
from django.contrib.auth.models import User     # this is used to get the user object

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts' 
    ordering = ['-date_posted']         # newest to oldest
    paginate_by = 5                     # 5 posts per page

class UserPostListView(ListView):             # This view will display all posts by a specific user
    model = Post
    template_name = 'blog/user_posts.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts' 
    paginate_by = 5                           # 5 posts per page

    def get_queryset(self):                   # This method will get the user object and return all posts by that user
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # Override form_valid method to set author of post to current user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # Override form_valid method to set author of post to current user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # this will redirect to home page after deleting a post
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

