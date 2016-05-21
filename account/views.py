from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

import datetime
import math

from jobs import settings
from .forms import CompanyForm, UserForm, CompanyUpdateForm
from board.forms import PostForm
from board.models import Category, Post

import stripe
import logging

# Get an instance of the logger
logger = logging.getLogger(__name__)


def register(request):

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        company_form = CompanyForm(data=request.POST)

        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save()
            
            company = company_form.save(commit=False)
            company.user = user

            company.save()

            # Tries to generate stripe id
            # Not important that it gets generated here
            try:
                company.get_stripe_customer()
            except Exception, e:
                logger.error(e.message)

            user = authenticate(email=user_form.cleaned_data['email'],
                                password=user_form.cleaned_data['password'])

            login(request, user)
            return redirect('update_info')

        else:
            print user_form.errors, company_form.errors

    else:
        user_form = UserForm()
        company_form = CompanyForm()

    return render(request, 'account/register.html', {'user_form': user_form, 'company_form': company_form})


@login_required
def post_a_job(request, post_slug=None):

    context = {}

    if post_slug:
        context['post_slug'] = True
        post = get_object_or_404(Post, company=request.user.company, slug=post_slug)

    if request.method == 'POST':

        if post_slug:
            form = PostForm(request.POST, instance=post)
        else:
            form = PostForm(request.POST)

        if form.is_valid():
            if len(form.cleaned_data['categories']) > 3:
                form.add_error('categories', forms.ValidationError("Only up to three categories are allowed", code="invalid"))
            else:
                if post_slug:
                    form.save()

                    return redirect('job_details', request.user.company.slug, post.slug)
                else:
                    post = form.save(commit=False)
                    post.company = request.user.company
                    post.date = datetime.date.today()
                    post.save()

                    # Post needs to be created before many-to-one relationship can be created
                    post.categories = form.cleaned_data['categories']
                    post.save()

                    return redirect('index')
        else:
            print form.errors
    else:
        if post_slug:
            form = PostForm(instance=post)
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


@login_required
def checkout(request, post_slug=None):
    context = {}

    company = request.user.company
    post = get_object_or_404(Post, company=company, slug=post_slug)

    # Makes sure the user doesn't pay for a post twice
    if post.paid:
        return redirect('job_details', company_slug=company.slug, post_slug=post.slug)

    error = None
    customer = None
    try:
        customer = company.get_stripe_customer()
    except Exception as error:
        error = "Can't connect to payment processing"

    if not error and request.method == 'POST':

        # Subscribe them to the job
        token = request.POST.get("stripeToken", "")

        # if they inputted a new card, or otherwise
        if token:
            try:
                company.subscribe_user(settings.STRIPE_PLAN_NAME, customer=customer, token=token)

                post.paid = True
                post.save()
            except stripe.error.CardError as error:
                error = "Credit card declined. Try using a new one."
            except Exception as Error:
                error = "An error occurred."
        else:
            # TODO - make sure that the customer actually has previous payments
            try:
                company.subscribe_user(settings.STRIPE_PLAN_NAME, customer=customer)

                post.paid = True
                post.save()
            except stripe.error.CardError as error:
                error = "Credit card declined. Try using a new one."
            except Exception as Error:
                error = "An error occurred."

    if customer:
        try:
            context['four_digits'] = company.get_four_digits(customer=customer)
        except Exception as error:
            error = "Can't get previous card info"

    context['pushable_key'] = settings.STRIPE_PUSHABLE_KEY
    context['post'] = post
    context['error'] = error

    return render(request, 'account/checkout.html', context)

@login_required
def update_info(request):
    context = {}

    message = None
    update_success = False

    company = request.user.company

    if request.method == 'POST':
        form = CompanyUpdateForm(request.POST, request.FILES)

        if form.is_valid():
            company.website = form.cleaned_data['website']
            company.description = form.cleaned_data['description']
            company.location = form.cleaned_data['location']

            # This is used since if the user doesn't upload anything, it's None.
            # If they click clear, it is False
            picture = form.cleaned_data['picture']
            if picture is not None:
                company.picture = form.cleaned_data['picture']

            company.save()

            message = "Company settings updated successfully"
            update_success = True
        else:
            print form.errors
            message = "Company settings failed, look for errors below"
    else:
        referer = request.META.get('HTTP_REFERER')
        if referer and '/account/password-change/' in referer:
            message = "Password updated successfully"
            update_success = True

        form = CompanyUpdateForm(initial={'description': company.description, 'website': company.website, 'location': company.location, 'picture': company.picture})

    context['company'] = company
    context['form'] = form
    context['allowed_tags'] = ", ".join(settings.ALLOWED_TAGS)

    if message:
        context['message'] = message
        context['update_success'] = update_success

    return render(request, 'account/update_info.html', context)


@login_required
def update_posts_base(request):

    context = {}

    company = request.user.company
    context['company'] = company
    context['posts'] = company.post_set.all()

    return render(request, 'account/update_posts_base.html', context)


def company_logout(request):

    logout(request)

    return redirect('index')


def company_login(request):

    context = {}

    if request.user.is_authenticated():
        return redirect('update_info')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('update_info')

        else:
            context['issues'] = True

    return render(request, 'account/login.html', context)


def password_reset_done(request):

    return render(request, 'account/password/password_reset_done.html')


def password_reset_complete(request):

    return redirect('login')
