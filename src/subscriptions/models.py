from django.db import models
from django.contrib.auth.models import Group,Permission
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from helpers.billing import create_product,create_product_price

User = get_user_model()

ALLOW_CUSTOM_GROUP = True

SUBSCRIPTION_PERMISSIONS =[
            ("advanced","Advanced Perm"),
            ("pro","Pro Perm"),
            ("basic","Basic Plan")
        ]


RAW=False
class Subscription(models.Model):
    '''
    Stripe subscription
    '''
    name = models.CharField(max_length=120)
    groups = models.ManyToManyField(Group)
    active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(Permission,limit_choices_to={'content_type__app_label':"subscriptions","codename__in":[permission[0] for permission in SUBSCRIPTION_PERMISSIONS]})
    stripe_id = models.CharField(max_length=120,null=True,blank=True)


    def save(self,*args,**kwargs):
        if not self.stripe_id:
            stripe_response = create_product(name=self.name,metadata={"subscription_plan_id":self.id},raw=False)
            self.stripe_id = stripe_response

        super().save(*args,**kwargs)


        
        pass
    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS


    def __str__(self):
        return self.name







class SubscriptionPrice(models.Model):
    '''
    Stripe subscription price
    '''

    class IntervalChoices(models.TextChoices):
        MONTHLY = "month","Monthly"
        YEARLY = "year","Yearly"



    subscription = models.ForeignKey(Subscription,on_delete=models.SET_NULL,blank=True,null=True)
    stripe_id = models.CharField(max_length=120,null=True,blank=True)
    interval = models.CharField(max_length=120,default=IntervalChoices.MONTHLY,choices=IntervalChoices.choices)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    order = models.IntegerField(default=-1,help_text="Ordering on Django pricing page")
    featured = models.BooleanField(default=True,help_text="Featured on Django pricing page")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id

    @property
    def stripe_currency(self):
        return "usd"

    @property
    def stripe_price(self):

        return self.price*100



    def save(self,*args,**kwargs):
        if (self.stripe_id is None and 
            self.product_stripe_id is not None):
            stripe = create_product_price(
                interval=self.interval,
                product=self.product_stripe_id,
                price=self.stripe_price,currency_type=self.stripe_currency,
                metadata={"subscription_plan_price_id":self.id},
                raw=RAW
                )

            self.stripe_id = stripe

        super().save(*args,**kwargs)

        if self.featured and self.subscription:
            qs = SubscriptionPrice.objects.filter(
                subscription=self.subscription,
                interval= self.interval
            ).exclude(id=self.id)
            qs.update(featured=False)








        
        





class UserSubscription(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription,on_delete=models.SET_NULL,null=True,blank=True)
    active = models.BooleanField(default=True)




def user_sub_post_save(sender,instance,*args,**kwargs):

    # instance of UserSubscription
    user_sub_instance = instance 

    # user instance 
    user = user_sub_instance.user

    # instance of Subscription
    subscription_obj = user_sub_instance.subscription
    groups_ids = []

    if subscription_obj is not None:
        # get all group linked with this scubscriptions
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list('id',flat=True)




    if not ALLOW_CUSTOM_GROUP:
        # set those group to that user.
        user.groups.set(groups)
    else:
        # get all subscriptions list without that is going to be subscribed
        subs_qs = Subscription.objects.filter(active=True)
        
        if subscription_obj is not None:
            subs_qs.exclude(id=subscription_obj.id)

        # filtered subscription groups id in list
        subs_groups = subs_qs.values_list("groups__id",flat=True)

        # set those value
        subs_groups_set = set(subs_groups)

        # all groups id in list
        # groups_ids = groups.values_list('id',flat=True)

        # user all groups id in list
        currrent_groups = user.groups.all().values_list('id',flat=True)

        # set both groups list and user group list
        groups_ids_set = set(groups_ids)

        # removing subs_group_set from all group
        current_groups_set = set(currrent_groups) - subs_groups_set

        # final list = user group | all groups
        final_group_ids = list(groups_ids_set | current_groups_set)
        user.groups.set(final_group_ids)



post_save.connect(user_sub_post_save,sender=UserSubscription)