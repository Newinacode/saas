from django.db import models
from django.contrib.auth import get_user_model
from helpers.billing import create_customer

from allauth.account.signals import (
    user_signed_up as allauth_user_signed_up,
    email_confirmed as allauth_email_confirmed
)

User = get_user_model()

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120,null=True,blank=True)
    init_email = models.EmailField(blank=True,null=True)
    init_email_confirmed = models.BooleanField(default=False)



    def save(self,*args,**kwargs):
        email = self.user.email
        if not self.stripe_id:
            if self.init_email_confirmed and self.init_email:
                if email != "" and email is not None:
                    
                    stripe_id = create_customer(email=email,
                    metadata={"user_id":self.user.id},
                    raw=False
                    )

                    self.stripe_id = stripe_id
        super().save(*args,**kwargs)
        




    def __str__(self):
        return f"{self.user.username}"




def allauth_user_signed_up_handler(request,user,*args,**kwargs):
    email = user.email
    Customer.objects.create(
        user = user,
        init_email = email,
        init_email_confirmed = False
    )
    

def allauth_email_confirmed_handler(request,email_address,*args,**kwargs):
    qs = Customer.objects.filter(init_email=email_address,init_email_confirmed=False)

    for obj in qs:
        obj.init_email_confirmed = True
        obj.save()

allauth_user_signed_up.connect(allauth_user_signed_up_handler)
allauth_email_confirmed.connect(allauth_email_confirmed_handler)
