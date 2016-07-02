from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from .models import Post, Category, Company, JobType
from endless_pagination.decorators import page_template
from jobs import settings
from account.models import Plan

import logging

# Get an instance of the logger
logger = logging.getLogger(__name__)


@page_template('board/single_post_index.html')  # just add this decorator
def index(request, category_slug=None, job_type_slug=None, template='board/index.html', extra_context=None):
    context = {}

    if category_slug:
        context['posts'] = get_valid_posts().filter(categories__slug=category_slug).order_by('-date', '-id')
        context['category_slug'] = category_slug
    elif job_type_slug:
        context['posts'] = get_valid_posts().filter(job_type__slug=job_type_slug).order_by('-date', '-id')
        context['job_type_slug'] = job_type_slug
    else:
        context['posts'] = get_valid_posts().order_by('-date', '-id')

    # Sort the categories from most to least jobs
    category_tuples = []
    for category in Category.objects.all():
        category_tuples.append((category, len(get_valid_category_posts(category))))

    context['categories'] = sorted(category_tuples, key=lambda cat: cat[1], reverse=True)[:5]

    # Sort the companies from most to least jobs
    company_tuples = []
    for company in Company.objects.all():
        count = len(get_valid_company_posts(company))
        if count > 0:
            company_tuples.append((company, count))

    context['companies'] = sorted(company_tuples, key=lambda comp: comp[1], reverse=True)[:5]

    # Sort the job types from most to least job types
    job_type_tuples = []
    for job_type in JobType.objects.all():
        count = len(get_valid_job_type_posts(job_type))
        job_type_tuples.append((job_type, count))

    context['job_types'] = sorted(job_type_tuples, key=lambda job: job[1], reverse=True)[:5]

    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


def company_plans(request):
    context = {}

    context['plans'] = Plan.objects.all().order_by('cost').filter(visible=True)

    if not request.user.is_anonymous():
        company = request.user.company
        context['company'] = company

        # If the user request to be downgraded to a post with no cost
        if request.method == 'POST':
            plan = get_object_or_404(Plan, slug=request.POST.get("plan", ""), cost=0)
            print plan.name

            # Update the companies plan and remove other subscriptions
            company.plan = plan
            company.remove_subscriptions()
            company.save()

            # Turn off all of the company's posts
            for post in company.post_set.all():
                post.paid = False
                post.save()

            return redirect('update_posts')

    return render(request, 'board/company_plans.html', context)


def categories(request):
    context = {}

    # Gets all categories and counts in alphabetical order that have more than 0 valid posts
    context['categories'] = []
    for category in Category.objects.all().order_by('name'):
        valid_posts_len = len(get_valid_category_posts(category))
        if valid_posts_len > 0:
            context['categories'].append((category, valid_posts_len))

    return render(request, 'board/categories.html', context)


def company_list(request):
    context = {}

    # Gets all companies and counts in alphabetical order that have more than 0 valid posts
    context['companies'] = []
    for company in Company.objects.all().order_by('name'):
        valid_posts_len = len(get_valid_company_posts(company))
        if valid_posts_len > 0:
            context['companies'].append((company, valid_posts_len))

    return render(request, 'board/company_list.html', context)


def job_details(request, company_slug, post_slug):

    context = {}

    context['job'] = get_object_or_404(Post, slug=post_slug, company__slug=company_slug)

    return render(request, 'board/job_details.html', context)


def company_details(request, company_slug):

    context = {}

    context['company'] = get_object_or_404(Company, slug=company_slug)

    context['jobs'] = get_valid_company_posts(context['company'])

    return render(request, 'board/company_details.html', context)


def about_us(request):
    return render(request, 'board/information/about.html')


def contact_us(request):
    return render(request, 'board/information/contact.html')


def page_not_found(request):
    return render(request, 'general/404.html')


# Views for the launch parts of the site
def employers_only_index(request):
    return render(request, 'launch/index.html')


def not_viewable_launch(request, category_slug=None, job_type_slug=None):
    return render(request, 'launch/not_viewable.html')


def get_valid_posts():
    return Post.objects.filter(paid=True, verified=True)


def get_valid_category_posts(category):
    return category.post_set.filter(paid=True, verified=True)


def get_valid_company_posts(company):
    return company.post_set.filter(paid=True, verified=True)


def get_valid_job_type_posts(job_type):
    return Post.objects.filter(paid=True, verified=True, job_type=job_type)