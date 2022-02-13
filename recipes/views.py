from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q, F

from recipes.models import Post, Category, Tag, PostImage
from .forms import PostForm


class Start(LoginView):
    template_name = 'registration/login.html'

    def get_queryset(self):
        return Post.objects.all()


class Home(ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recipes'
        return context


class PostsByCategory(ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    paginate_by = 20
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByTag(ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    paginate_by = 20
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recipes by tag: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class ShowPost(DetailView):
    template_name = 'recipes/single.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # post = Post.objects.create(**form.cleaned_data)
            post = form.save()
            return redirect(post)

    else:
        form = PostForm()
    return render(request, 'recipes/add_post.html', {'form': form})




class Search(ListView):
    template_name = 'recipes/search.html'
    context_object_name = 'posts'
    paginate_by = 40

    def get_queryset(self):
        if self.request.GET.get('s').isdigit():
            return Post.objects.filter(id=self.request.GET.get('s'), is_published=True)
        else:
            return Post.objects.filter(
                Q(title__icontains=self.request.GET.get('s'), is_published=True)
                | Q(id__icontains=self.request.GET.get('s'), is_published=True)
                | Q(ingredients__icontains=self.request.GET.get('s'), is_published=True)
                | Q(content__icontains=self.request.GET.get('s'), is_published=True)
            )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['search_word'] = self.request.GET.get('s')
        return context


class PostsByCooked(ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.filter(cooked=True, is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cooked recipes'
        return context


class PostsByFavorites(ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.filter(favorites=True, is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Favorites'
        return context