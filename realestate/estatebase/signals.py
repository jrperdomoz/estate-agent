from django.db.models.signals import post_save, pre_save, post_delete
from django.db import transaction
from estatebase.models import Bidg, Stead, YES, EstateType, Estate,\
    prepare_history, Bid, Contact, EstateClient, Client, BidEvent

def prepare_estate_childs(sender, instance, created, **kwargs):
    if created:
        estate_type = getattr(instance,'_estate_type_id', None) and EstateType.objects.get(pk=instance._estate_type_id) or None                
        if estate_type:             
            if estate_type.estate_type_category.has_bidg == YES:
                Bidg.objects.create(estate=instance, estate_type=estate_type, basic=True)
            if estate_type.estate_type_category.has_stead == YES:
                stead_type_id = instance.estate_category.is_stead and estate_type.pk or Stead.DEFAULT_TYPE_ID 
                Stead.objects.create(estate=instance, estate_type_id=stead_type_id)          

def set_validity(sender, instance, created, **kwargs):
    estate = getattr(instance,'estate',instance) 
    post_save.disconnect(set_validity, sender=Estate)
    estate.set_validity(estate.check_validity())
    estate.save()
    post_save.connect(set_validity, sender=Estate)

def estate_client_handler(sender, instance, **kwargs):    
    instance.estate.set_contact()
    instance.estate.save()        

def update_deleted(sender, instance, created, **kwargs):
    if instance.deleted:                     
        for estate in instance.estates.all():
            estate.set_contact()
            estate.save()            
            prepare_history(estate.history, instance._user_id)                                

@transaction.commit_on_success        
def update_estate(sender, instance, created, **kwargs):
    if instance.client.history:
        prepare_history(instance.client.history, instance.user_id)
    if instance.client.pk:    
        for estate in instance.client.estates.all():
            estate.set_contact()
            estate.save()            
            prepare_history(estate.history, instance.user_id)                                

def update_localities(sender, instance, **kwargs):
    if instance.pk:
        if instance.regions.all().count() > 0 and not instance.localities.all().count() > 0:
            for region in instance.regions.all():
                for locality in region.locality_set.all(): 
                    instance.localities.add(locality)
                    instance.estate_filter.update({'locality_1' : locality.pk})                    

def bid_event_history(sender, instance, created, **kwargs):
    if created:
        post_save.disconnect(bid_event_history, sender=BidEvent)
        instance.history = prepare_history(None, instance._user_id)
        instance.save()
        post_save.connect(bid_event_history, sender=BidEvent)
    else:
        prepare_history(instance.history, instance._user_id)

def connect_signals():
    post_save.connect(prepare_estate_childs, sender=Estate)
    post_save.connect(set_validity, sender=Estate)
    post_save.connect(set_validity, sender=Bidg)
    post_save.connect(set_validity, sender=Stead)
    post_save.connect(update_deleted, sender=Client)
    post_save.connect(update_estate, sender=Contact)
    post_save.connect(estate_client_handler, sender=EstateClient)
    post_delete.connect(estate_client_handler, sender=EstateClient)
    pre_save.connect(update_localities, sender=Bid)
    post_save.connect(bid_event_history, sender=BidEvent)