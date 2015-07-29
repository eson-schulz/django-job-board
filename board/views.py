from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from .forms import PostForm
from .models import Post, Category
from endless_pagination.decorators import page_template


@page_template('single_post_index.html')  # just add this decorator
def index(
        request, template='index.html', extra_context=None):
    context = {
        'posts': Post.objects.all(),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


def post_a_job(request):

    context = {}

    if request.method == 'POST':
        form = PostForm(request.POST)

    else:
        form = PostForm()

    context['form'] = form
    context['category_column_size'] = int(len(Category.objects.all()) / 3)
    print context['category_column_size']
    return render(request, 'job_post.html', context)


def page_not_found(request):
    return render(request, '404.html')