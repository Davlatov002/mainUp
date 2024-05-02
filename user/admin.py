from django.contrib import admin
from .models import Identified, Profile, MoneyOut, Transaction, Strength
from django.utils.html import format_html
from datetime import datetime
from django.contrib import messages
import time
from . import serialazers

def make_identified(modeladmin, request, queryset):
    for obj in queryset:
        if obj.is_identified != True:
            a = obj.user.id
            profile = Profile.objects.get(id=a)
            link = profile.friend_referal_link
            profile.is_identified = True
            obj.is_identified = True
            obj.save()
            profile.save()
            if link != None:
                profile.balance_netbo += 0.2
                pr_username = profile.username
                profile.save()
                taim = int(time.time())
                data = {"username":pr_username,'balance_netbo':0.2,"created_at":taim}
                tran = serialazers.Tranzaktionserialazer(data=data)
                if tran.is_valid():
                    tran.save()

                frend = Profile.objects.get(referal_link=link)
                frend.number_people += 1
                frend.balance_netbo += 0.1
                fr_username = frend.username
                data = {"username":fr_username,'balance_netbo':0.1,"created_at":taim}
                frend.save()
                tran = serialazers.Tranzaktionserialazer(data=data)
                if tran.is_valid():
                    tran.save()

make_identified.short_description = "Mark selected as identified"


class IdentifiedAdmin(admin.ModelAdmin):
    list_display = ('fullname','is_identified')
    search_fields = ('user__username',)
    list_filter = (('is_identified', admin.BooleanFieldListFilter), )
    readonly_fields = ('display_iD_image','display_address_image', 'display_selfie_image')
    actions = [make_identified]

    def display_iD_image(self, obj):
        return format_html('<img src="{}" width="300" height="300" />'.format(obj.id_image.url))
    display_iD_image.short_description = 'ID Image'

    def display_address_image(self, obj):
        return format_html('<img src="{}" width="300" height="300" />'.format(obj.address_image.url))
    display_address_image.short_description = 'Address Image'

    def display_selfie_image(self, obj):
        return format_html('<img src="{}" width="300" height="300" />'.format(obj.selfie_image.url))
    display_selfie_image.short_description = 'Selfie Image'

    def save_model(self, request, obj, form, change):
        if 'is_identified' in form.changed_data and form.cleaned_data['is_identified'] == True:
            a = form.cleaned_data['user'].id
            profile = Profile.objects.get(id=a)
            link = profile.friend_referal_link
            profile.is_identified = True
            profile.save()
            if link != None:
                profile.balance_netbo += 0.2
                pr_username = profile.username
                profile.save()
                taim = int(time.time())
                data = {"username":pr_username,'balance_netbo':0.2,"created_at":taim}
                tran = serialazers.Tranzaktionserialazer(data=data)
                if tran.is_valid():
                    tran.save()

                frend = Profile.objects.get(referal_link=link)
                frend.number_people += 1
                frend.balance_netbo += 0.1
                fr_username = frend.username
                data = {"username":fr_username,'balance_netbo':0.1,"created_at":taim}
                frend.save()
                tran = serialazers.Tranzaktionserialazer(data=data)
                if tran.is_valid():
                    tran.save()
        else:
            a = form.cleaned_data['user'].id
            profile = Profile.objects.get(id=a)
            profile.is_identified = False
            profile.save()
        super().save_model(request, obj, form, change)

class ModelOutAdmin(admin.ModelAdmin):
    list_display = ('user','is_identified', 'formatted_created_at')
    list_filter = (('is_identified', admin.BooleanFieldListFilter), )
    search_fields = ('user__username',)

    def save_model(self, request, obj, form, change):
        if 'is_identified' in form.changed_data and form.cleaned_data['is_identified'] == False:
            a = form.cleaned_data['user']
            profile = Profile.objects.get(id=a)
            b = form.cleaned_data['balance_netbo']
            profile.balance_netbo += b
            profile.save()
        super().save_model(request, obj, form, change)
    
    def formatted_created_at(self, obj):
        # Avvalgi vaqt ma'lumotini datetime obyektiga o'zgartiramiz
        created_at_datetime = datetime.fromtimestamp(obj.created_at)
        return created_at_datetime.strftime("%Y-%m-%d %H:%M:%S")
    formatted_created_at.short_description = 'Created At'






class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_identified', 'balance_netbo', 'number_people')
    search_fields = ('username','email')
    list_filter = (('is_identified', admin.BooleanFieldListFilter),)
    ordering = ('balance_netbo','number_people')



class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'balance_netbo', 'formatted_created_at')
    search_fields = ('user__username',)

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User'

    def formatted_created_at(self, obj):
        # Avvalgi vaqt ma'lumotini datetime obyektiga o'zgartiramiz
        created_at_datetime = datetime.fromtimestamp(obj.created_at)
        return created_at_datetime.strftime("%Y-%m-%d %H:%M:%S")
    formatted_created_at.short_description = 'Created At'

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Identified, IdentifiedAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(MoneyOut, ModelOutAdmin)
admin.site.register(Strength)