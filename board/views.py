import datetime
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from .forms import PostForm
from .models import Post, Category, Company
from endless_pagination.decorators import page_template
import math
from jobs import settings


@page_template('single_post_index.html')  # just add this decorator
def index(
        request, template='index.html', extra_context=None):
    context = {
        'posts': Post.objects.order_by('-date'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


def post_a_job(request):

    context = {}

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.company = Company.objects.get(id=1)
            post.date = datetime.date.today()
            post.save()

            return redirect('index')
        else:
            print form.errors
    else:
        form = PostForm()

    context['form'] = form
    context['category_column_size'] = int(math.ceil(len(Category.objects.all()) / 3.0))
    context['allowed_tags'] = ", ".join(settings.ALLOWED_TAGS)

    # Decides what the second column size should be
    if len(Category.objects.all()) - (context['category_column_size'] * 2) < (context['category_column_size'] - 1):
        context['category_column_2_size'] = (context['category_column_size'] * 2) - 1
    else:
        context['category_column_2_size'] = context['category_column_size'] * 2

    return render(request, 'job_post.html', context)


def job_details(request, company_slug, post_slug):

    context = {}

    context['job'] = get_object_or_404(Post, slug=post_slug, company__slug=company_slug)

    return render(request, 'job_details.html', context)


def company_details(request, company_slug):

    context = {}

    context['company'] = get_object_or_404(Company, slug=company_slug)

    context['jobs'] = context['company'].post_set.all()

    return render(request, 'company_details.html', context)


def page_not_found(request):
    return render(request, '404.html')