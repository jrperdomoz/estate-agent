from estatebase.models import Street, Locality, Microdistrict, EstateType, \
    Estate, Region, EstateStatus, WallConstrucion, Origin, Beside, Interior, \
    Electricity, Watersupply, Gassupply, Sewerage, Driveway, Client, Contact, ExUser, \
    ClientType, Bid, EstateRegister, EstateTypeCategory, Internet, Telephony, \
    LayoutType, LevelName, ComStatus, EstateClientStatus, Shape, EstateParam,\
    Validity, Appliance, BidEventCategory, RegisterCategory, ExteriorFinish,\
    BidStatus, Purpose, Heating, YandexBuilding, DealStatus
from selectable.base import ModelLookup
from selectable.exceptions import LookupAlreadyRegistered
from selectable.registry import registry
import re

class SimpleIdLookup(ModelLookup):
    search_fields = ('id__exact',)
    def get_item_label(self, item):
        if hasattr(item, 'name'):            
            return u"%s, %s" % (item.pk, getattr(item, 'name'))
        else:
            return u"%s" % item.pk        
    def get_item_value(self, item):
        return u"%s" % (item.pk,)
    def get_query(self, request, term):
        term = re.sub(r'\D', '', term)
        return super(SimpleIdLookup, self).get_query(request, term)        

class ClientIdLookup(SimpleIdLookup):
    model = Client

class EstateRegisterIdLookup(SimpleIdLookup):
    model = EstateRegister    

class BidIdLookup(SimpleIdLookup):
    model = Bid

class SimpleNameLookup(ModelLookup):
    search_fields = ('name__icontains',)
    
class EstateLookup(ModelLookup):
    model = Estate
    search_fields = ('id__exact',)
    def get_query(self, request, term):
        term = re.sub(r'\D', '', term)
        results = super(EstateLookup, self).get_query(request, term)        
        if request.user:
            results = results.filter(region__geo_group__userprofile__user__exact=request.user)
        return results        
    
class EstateStatusLookup(ModelLookup):
    model = EstateStatus
    search_fields = ('name__icontains',)    
    
class RegionLookup(ModelLookup):
    model = Region
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(RegionLookup, self).get_query(request, term)        
        if request.user:
            results = results.filter(geo_group__userprofile__user__exact=request.user)
        return results

class StreetLookup(ModelLookup):
    model = Street
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(StreetLookup, self).get_query(request, term)
        locality = request.GET.get('locality', '')
        if locality:
            results = results.filter(locality=locality)
        return results
    def get_item_label(self, item):
        return u"%s, %s" % (item, item.locality)

class MicrodistrictLookup(StreetLookup):
    model = Microdistrict

class LocalityLookup(ModelLookup):
    model = Locality
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(LocalityLookup, self).get_query(request, term)
        region = request.GET.get('region', '')
        if region:
            results = results.filter(region=region)
        return results
    def get_item_label(self, item):
        return u"%s, %s" % (item.name, item.region or '')

class EstateTypeCategoryLookup(ModelLookup):
    search_fields = ('name__icontains',)
    model = EstateTypeCategory
    def get_query(self, request, term):
        results = super(EstateTypeCategoryLookup, self).get_query(request, term)
        return results.filter(independent=True)

class EstateTypeLookup(SimpleNameLookup):   
    model = EstateType 
    independence = True
    def get_query(self, request, term):
        results = super(EstateTypeLookup, self).get_query(request, term)
        results = results.filter(estate_type_category__independent=self.independence)        
        self.category = request.GET.get('category', '')        
        if self.category:
            results = results.filter(estate_type_category_id=self.category)
        return results
    def get_item_label(self, item):
        if self.category:
            return u"%s" % (item.name)
        return u"%s, %s" % (item.name, item.estate_type_category or '')

class OutbuildingLookup(EstateTypeLookup):
    independence = False

class WallConstrucionLookup(SimpleNameLookup):
    model = WallConstrucion       

class OriginLookup(SimpleNameLookup):
    model = Origin    
    
class BesideLookup(SimpleNameLookup):
    model = Beside      

class InteriorLookup(SimpleNameLookup):
    model = Interior    
    
class ElectricityLookup(SimpleNameLookup):
    model = Electricity    

class WatersupplyLookup(SimpleNameLookup):
    model = Watersupply

class GassupplyLookup(SimpleNameLookup):
    model = Gassupply

class SewerageLookup(SimpleNameLookup):
    model = Sewerage

class DrivewayLookup(SimpleNameLookup):
    model = Driveway

class HeatingLookup(SimpleNameLookup):
    model = Heating

class ClientLookup(ModelLookup):
    model = Client
    search_fields = ('name__icontains', 'address__icontains', 'contacts__contact__icontains')
    def get_query(self, request, term):
        results = super(ClientLookup, self).get_query(request, term)
        return results.distinct('id')    
    def get_item_label(self, item):
        contacts = ', '.join(item.contacts.all().values_list('contact', flat=True))
        address = item.address and ('(%s)' % item.address)  or ''
        return u"%s: %s %s" % (item.name, contacts or '', address)

class ClientTypeLookup(SimpleNameLookup):
    model = ClientType    
    
class ContactLookup(ModelLookup):
    model = Contact
    search_fields = ('contact__icontains',)

class ExUserLookup(ModelLookup):
    model = ExUser
    search_fields = ('username__icontains', 'first_name__icontains', 'last_name__icontains', 'email__icontains')
    
class ComChoiceLookup(SimpleNameLookup):
    model = ComStatus

class InternetLookup(SimpleNameLookup):
    model = Internet 

class TelephonyLookup(SimpleNameLookup):
    model = Telephony

class LayoutTypeLookup(SimpleNameLookup):
    model = LayoutType
    
class LevelNameLookup(SimpleNameLookup):
    model = LevelName    
    
class EstateClientStatusLookup(SimpleNameLookup):
    model = EstateClientStatus    

class ShapeLookup(SimpleNameLookup):
    model = Shape    
    
class EstateParamLookup(SimpleNameLookup):
    model = EstateParam
    
class ValidityLookup(SimpleNameLookup):
    model = Validity    

class ApplianceLookup(SimpleNameLookup):
    model = Appliance 

class BidEventCategoryLookup(SimpleNameLookup):
    model = BidEventCategory    

class RegisterCategoryLookup(SimpleNameLookup):
    model = RegisterCategory
    
class ExteriorFinishLookup(SimpleNameLookup):
    model = ExteriorFinish    

class BidStatusLookup(SimpleNameLookup):
    model = BidStatus

class PurposeLookup(SimpleNameLookup):
    model = Purpose

class YandexBuildingLookup(SimpleNameLookup):
    model = YandexBuilding    

class DealStatusLookup(SimpleNameLookup):
    model = DealStatus    
    
try:
    registry.register(StreetLookup)
    registry.register(LocalityLookup)
    registry.register(MicrodistrictLookup)
    registry.register(EstateTypeLookup)
    registry.register(EstateLookup)
    registry.register(RegionLookup)
    registry.register(EstateStatusLookup)   
    registry.register(WallConstrucionLookup) 
    registry.register(OriginLookup)   
    registry.register(BesideLookup)
    registry.register(InteriorLookup)
    registry.register(ElectricityLookup)
    registry.register(WatersupplyLookup)    
    registry.register(GassupplyLookup)
    registry.register(SewerageLookup)
    registry.register(DrivewayLookup)
    registry.register(ClientLookup)
    registry.register(ContactLookup)
    registry.register(ExUserLookup)
    registry.register(ClientIdLookup)
    registry.register(ClientTypeLookup)
    registry.register(BidIdLookup)
    registry.register(EstateRegisterIdLookup)
    registry.register(EstateTypeCategoryLookup)
    registry.register(ComChoiceLookup)
    registry.register(InternetLookup)
    registry.register(TelephonyLookup)
    registry.register(LayoutTypeLookup)
    registry.register(LevelNameLookup)    
    registry.register(EstateClientStatusLookup)    
    registry.register(ShapeLookup)      
    registry.register(EstateParamLookup)
    registry.register(ValidityLookup)
    registry.register(ApplianceLookup)
    registry.register(BidEventCategoryLookup)
    registry.register(RegisterCategoryLookup)
    registry.register(ExteriorFinishLookup)
    registry.register(BidStatusLookup)
    registry.register(OutbuildingLookup)
    registry.register(PurposeLookup)
    registry.register(HeatingLookup) 
    registry.register(YandexBuildingLookup)   
    registry.register(DealStatusLookup)
    
except LookupAlreadyRegistered:
    pass    
