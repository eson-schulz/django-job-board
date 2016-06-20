from django.db import models
from django.template.defaultfilters import slugify
from email_user.models import EmailUser

import itertools
import stripe
import logging

# Get an instance of the logger
logger = logging.getLogger(__name__)


class Company(models.Model):
    user = models.OneToOneField(EmailUser)

    name = models.CharField(max_length=60)
    picture = models.ImageField(blank=True, upload_to="companies/")
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(blank=True, max_length=30, default="Owatonna, MN")
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    # Used for Stripe communication
    stripe_id = models.CharField(max_length=50, blank=True, null=True)

    slug = models.SlugField(unique=True)

    plan = models.ForeignKey('Plan')

    # Returns a value of how many posts a user can have based off their plan
    def max_posts(self):
        return self.plan.max_posts

    # Returns a boolean telling whether or not the company can enable any more posts
    def can_post(self):
        return self.max_posts() > len(self.post_set.filter(paid=True))

    # Gets the stripe customer associated with this company. If it doesn't exist, attempt to create a new one
    def get_stripe_customer(self):
        try:
            if not self.stripe_id:
                customer = stripe.Customer.create(
                    email=self.user.email,
                    description=self.name
                )

                self.stripe_id = customer.id
                self.save()

                return customer
            else:
                return stripe.Customer.retrieve(self.stripe_id)

        except (stripe.error.CardError, stripe.error.APIConnectionError, stripe.error.APIError,
                stripe.error.AuthenticationError, stripe.error.InvalidRequestError,
                stripe.error.RateLimitError, stripe.error.StripeError) as error:
            logger.error(error.message)
            raise

    # Returns the 4 digits of the attached credit card
    # No exceptions, just None if there was an error
    def get_four_digits(self, customer=None):
        if not self.stripe_id:
            return None

        try:
            if not customer:
                customer = self.get_stripe_customer()

            if customer.default_source:
                card = customer.sources.retrieve(customer.default_source)
                return card.last4

        except (stripe.error.CardError, stripe.error.APIConnectionError, stripe.error.APIError,
                stripe.error.AuthenticationError, stripe.error.InvalidRequestError,
                stripe.error.RateLimitError, stripe.error.StripeError) as error:
            logger.error(error.message)
            raise

    # Subscribes the user to the given plan name
    # Makes sure to remove all other plans before subscribing to the new one
    def subscribe_user(self, plan_name, customer=None, token=None):
        try:
            # Try to generate customer if one doesn't exist
            if not customer:
                customer = self.get_stripe_customer()

            self.remove_subscriptions(customer=customer)

            customer.subscriptions.create(plan=plan_name, source=token)

        except (stripe.error.CardError, stripe.error.APIConnectionError, stripe.error.APIError,
                stripe.error.AuthenticationError, stripe.error.InvalidRequestError,
                stripe.error.RateLimitError, stripe.error.StripeError) as error:
            logger.error(error.message)
            raise

    # Removes all subscriptions from a stripe customer object
    def remove_subscriptions(self, customer=None):
        try:
            # Try to generate customer if one doesn't exist
            if not customer:
                customer = self.get_stripe_customer()

            for sub in customer.subscriptions.data:
                sub.delete()

        except (stripe.error.CardError, stripe.error.APIConnectionError, stripe.error.APIError,
                stripe.error.AuthenticationError, stripe.error.InvalidRequestError,
                stripe.error.RateLimitError, stripe.error.StripeError) as error:
            logger.error(error.message)
            raise

    def post_count(self):
        return len(self.post_set.all())

    def save(self, *args, **kwargs):

        if not self.id:
            max_length = 50

            self.slug = orig = slugify(self.name)[:max_length]

            for x in itertools.count(1):
                if not Company.objects.filter(slug=self.slug).exists():
                    break

                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        super(Company, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=20)
    stripe_id = models.CharField(max_length=20)

    max_posts = models.PositiveSmallIntegerField()
    max_upgraded_posts = models.PositiveSmallIntegerField()

    company_image = models.BooleanField(default=False)
    social_links = models.BooleanField(default=False)
    social_post = models.BooleanField(default=False)
    email_post = models.BooleanField(default=False)

    visible = models.BooleanField(default=True)

    cost = models.PositiveSmallIntegerField()

    def is_paid(self):
        return self.cost != 0;

    def __unicode__(self):
        return self.name