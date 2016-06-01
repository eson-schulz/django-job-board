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

    # Used for Stripe communication
    stripe_id = models.CharField(max_length=50, blank=True, null=True)

    slug = models.SlugField(unique=True)

    BASIC = 'B'
    ADVANCED = 'A'
    PREMIUM = 'P'
    CUSTOM = 'C'

    PLAN_CHOICES = (
        (BASIC, 'Basic'),
        (ADVANCED, 'Advanced'),
        (PREMIUM, 'Premium'),
        (CUSTOM, 'Custom')
    )

    plan = models.CharField(max_length=1, choices=PLAN_CHOICES, default=BASIC)


    # Returns a value of how many posts a user can have based off their plan
    def max_posts(self):
        if self.plan == self.BASIC:
            return 2
        elif self.plan == self.ADVANCED:
            return 5
        elif self.plan == self.PREMIUM:
            return 10
        elif self.plan == self.CUSTOM:
            return 20
        else:
            logger.error("Company " + self.name + " has an invalid plan: " + str(self.plan))
            return 0

    # Returns a boolean telling whether or not the company can enable any more posts
    def can_post(self):
        return self.max_posts() > len(self.post_set.filter(paid=True))

    # Returns a customer
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

    # Increases the subscription count for the user
    def subscribe_user(self, plan_name, customer=None, token=None):
        try:
            if not customer:
                customer = self.get_stripe_customer()

            subscription = None
            for sub in customer.subscriptions.data:
                if sub.plan.id == plan_name:
                    subscription = sub

            if not subscription:
                customer.subscriptions.create(plan=plan_name, source=token)
            else:
                if token:
                    subscription.source = token
                subscription.quantity += 1
                subscription.save()

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