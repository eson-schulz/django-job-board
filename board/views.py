import datetime
from django import forms
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from .forms import PostForm
from .models import Post, Category, Company
from endless_pagination.decorators import page_template
import math
from jobs import settings


@page_template('board/single_post_index.html')  # just add this decorator
def index(request, category_slug=None, template='board/index.html', extra_context=None):
    context = {}

    if category_slug:
        context['posts'] = Post.objects.filter(categories__slug=category_slug).order_by('-date', '-id')
        context['category_slug'] = category_slug
    else:
        context['posts'] = Post.objects.order_by('-date', '-id')

    # Sort the categories from most to least jobs
    category_tuples = []
    for category in Category.objects.all():
        category_tuples.append((category, len(category.post_set.all())))

    context['categories'] = sorted(category_tuples, key=lambda cat: cat[1], reverse=True)[:5]

    # Sort the companies from most to least jobs
    company_tuples = []
    for company in Company.objects.all():
        company_tuples.append((company, len(company.post_set.all())))

    context['companies'] = sorted(company_tuples, key=lambda comp: comp[1], reverse=True)[:5]

    # Sort the job types from most to least job types
    job_dict = {}
    for job_type in Post.JOB_TYPE_CHOICES:
        job_dict[job_type[0]] = 0

    # Create a count of job types
    for post in Post.objects.all():
        job_dict[post.job_type] += 1

    job_type_list = job_dict.items()

    # Convert job types from short name to full name
    for job_index in range(0, len(job_type_list)):
        for key, value in Post.JOB_TYPE_CHOICES:
            if key == job_type_list[job_index][0]:
                job_type_list[job_index] = (value, job_type_list[job_index][1])

    context['job_types'] = sorted(job_type_list, key=lambda job: job[1], reverse=True)[:5]

    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


def post_a_job(request):

    context = {}

    if request.user.is_authenticated():
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                if len(form.cleaned_data['categories']) > 3:
                    form.add_error('categories', forms.ValidationError("Only up to three categories are allowed", code="invalid"))
                else:
                    post = form.save(commit=False)
                    post.company = request.user.company
                    post.date = datetime.date.today()
                    post.save()

                    return redirect('index')
            else:
                print form.errors
        else:
            form = PostForm()

        context['form'] = form
        context['allowed_tags'] = ", ".join(settings.ALLOWED_TAGS)

        # Decides what the second column size should be
        context['category_column_size'] = int(math.ceil(len(Category.objects.all()) / 3.0))

        if len(Category.objects.all()) - (context['category_column_size'] * 2) < (context['category_column_size'] - 1):
            context['category_column_2_size'] = (context['category_column_size'] * 2) - 1
        else:
            context['category_column_2_size'] = context['category_column_size'] * 2

        return render(request, 'board/job_post.html', context)
    else:
        return redirect('login')


def categories(request):
    context = {}

    category_list = Category.objects.all()

    # Gets the number of posts associated with each category
    category_count = []
    for i in range(0, len(category_list)):
        count = len(category_list[i].post_set.all())

        if count > 0:
            category_count.append((category_list[i], count))

    context['categories'] = category_count

    # Decides what the second column size should be
    context['category_column_size'] = int(math.ceil(len(category_count) / 3.0))

    if len(Category.objects.all()) - (context['category_column_size'] * 2) < (context['category_column_size'] - 1):
        context['category_column_2_size'] = (context['category_column_size'] * 2) - 1
    else:
        context['category_column_2_size'] = context['category_column_size'] * 2

    return render(request, 'board/categories.html', context)


def job_details(request, company_slug, post_slug):

    context = {}

    context['job'] = get_object_or_404(Post, slug=post_slug, company__slug=company_slug)

    return render(request, 'board/job_details.html', context)


def company_details(request, company_slug):

    context = {}

    context['company'] = get_object_or_404(Company, slug=company_slug)

    context['jobs'] = context['company'].post_set.all()

    return render(request, 'board/company_details.html', context)


def page_not_found(request):
    return render(request, 'general/404.html')