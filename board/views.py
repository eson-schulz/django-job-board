from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from .models import Post
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

#def index(request):
#    context = {}

#    context['posts'] = Post.objects.all()

#    return render(request, 'index.html', context)


def page_not_found(request):
    return render(request, '404.html')