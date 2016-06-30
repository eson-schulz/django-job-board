from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

import datetime
import math

from jobs import settings
from .forms import CompanyForm, UserForm, CompanyUpdateForm
from board.forms import PostForm
from board.models import Category, Post
from .models import Plan

import logging
import stripe

# Get an instance of the logger
logger = logging.getLogger(__name__)


def register(request):

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        company_form = CompanyForm(data=request.POST)

        if len(Plan.objects.all()) == 0:
            logger.error("No posts are created, so a new user cannot be created")
            user_form.add_error("password", "Error in creating account. Contact administration. Mention PLANS")
        else:
            if user_form.is_valid() and company_form.is_valid():
                user = user_form.save()

                company = company_form.save(commit=False)
                company.user = user
                company.plan = Plan.objects.all().order_by("cost")[0]

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

    # Checks to see if we can post any more
    context['can_post'] = request.user.company.can_post()

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
                    
                    # Check to see if this is posted right away or not
                    if context['can_post']:
                        post.paid = True

                    if post.company.plan.cost != 0:
                        post.verified = True
                    
                    post.save()

                    # Post needs to be created before many-to-one relationship can be created
                    post.categories = form.cleaned_data['categories']
                    post.save()

                    # Send email to notify about verification being required
                    message = "New post on your site. " + request.user.company.name + " posted with title " + post.title
                    header = 'New Post'
                    if not post.verified:
                        header = 'Verification Required - Post'
                    try:
                        send_mail(header, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMINS[0][1]], fail_silently=True)
                    except Exception as e:
                        logger.error("Sending new post error: " + e.message)

                    return redirect('job_details', request.user.company.slug, post.slug)
        else:
            print form.errors
    else:
        if post_slug:
            form = PostForm(instance=post)
        else:
            form = PostForm(initial={"email": request.user.email})

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
            company.facebook_url = form.cleaned_data['facebook_url']
            company.twitter_url = form.cleaned_data['twitter_url']

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
        form = CompanyUpdateForm(initial={'description': company.description, 'website': company.website, 'location': company.location, 'picture': company.picture, 'facebook_url': company.facebook_url, 'twitter_url': company.twitter_url})

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

    # POST is used to switch the enabled on various posts
    # Checks to make sure post is owned by user, then
    # sees if they are enabling or disabling the post,
    # then does check to make sure they can enable/disable
    if request.method == 'POST':
        if request.POST.get('post'):
            post = Post.objects.get(id=request.POST.get('post'))
            if post and post.company.id == company.id:
                if post.paid:
                    post.paid = False
                    post.save()
                    context['success'] = True
                    context['message'] = post.title + " job successfully disabled"
                else:
                    if company.can_post():
                        post.paid = True
                        post.save()
                        context['success'] = True
                        context['message'] = post.title + " job successfully enabled"
                    else:
                        context['success'] = False
                        context['message'] = post.title + " job can't be enabled because the allowed posts limit has been reached. Upgrade to increase limit"
            else:
                context['success'] = False
                context['message'] = "Action can't be completed. If you think this is an error please contact us."
        else:
            context['success'] = False
            context['message'] = "Action can't be completed. If you think this is an error, please contact us."

    context['company'] = company
    context['posts'] = company.post_set.all()
    context['enabled_posts_count'] = len(company.post_set.filter(paid=True))

    return render(request, 'account/update_posts_base.html', context)


@login_required
def checkout(request, plan_slug):

    context = {}
    company = request.user.company
    context['company'] = company
    plan = get_object_or_404(Plan, slug=plan_slug)
    context['plan'] = plan

    if request.method == 'POST':
        error = None
        customer = None
        try:
            customer = company.get_stripe_customer()
        except Exception as error:
            error = "Can't connect to payment processing"

        # Subscribe them to the plan
        if not error and request.method == 'POST':

            # get the token from stripe (POST)
            token = request.POST.get("stripeToken", "")

            if token:
                try:
                    # Removes the old subscription and subscribes the user to the new one
                    company.subscribe_user(plan.stripe_id, customer=customer, token=token)

                    company.plan = plan
                    company.save()

                    context['success'] = True
                except stripe.error.CardError as error:
                    error = "Credit card declined. Try using a new one."
                except Exception as error:
                    logger.error(error.message)
                    error = "An error occurred."
            else:
                error = "Payment not received. Try again"

        context['error'] = error

    context['pushable_key'] = settings.STRIPE_PUSHABLE_KEY

    return render(request, 'account/checkout.html', context)


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


def password_change_complete(request):

    return render(request, 'account/password/password_change_complete.html')
