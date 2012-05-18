# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from models import EstateTypeCategory
from django.views.generic.edit import CreateView, ModelFormMixin, UpdateView,\
    DeleteView
from estatebase.forms import EstateForm, ClientForm, ContactFormSet,\
    ClientFilterForm
from estatebase.models import EstateType
from django.core.urlresolvers import reverse
from estatebase.models import Estate, Client
from estatebase.tables import EstateTable
from django_tables2.config import RequestConfig
from django.utils import simplejson as json
from django.http import HttpResponse, QueryDict
from django.views.generic.list import ListView

class AjaxMixin(ModelFormMixin):
    def serializer_json(self, data):
        """Returns json format"""
        return json.dumps(data), 'application/json'    

    def no_ajax_response(self):
        return HttpResponse('Waiting for ajax reqiest!')

    def response_alternative(self, form, success=True):
        if success:        
            return HttpResponse(json.dumps({'result': 'success'}))
        else:
            return HttpResponse(json.dumps({'form': form.as_p().replace('\n', ''), 'result': 'error'}))

    def form_valid(self, form):        
        if not self.request.is_ajax():
            return super(AjaxMixin, self).form_valid(form)
        self.object = form.save();
        return self.response_alternative(form)

    def form_invalid(self, form):        
        if not self.request.is_ajax():
            return super(AjaxMixin, self).form_invalid(form)
        return self.response_alternative(form, False)

class EstateTypeView(TemplateView):    
    template_name = 'index.html'        
    def get_context_data(self, **kwargs):
        context = super(EstateTypeView, self).get_context_data(**kwargs)                
        estate_categories = EstateTypeCategory.objects.all()
        context.update({
            'title': 'base',
            'estate_categories': estate_categories
        })        
        return context 

    
class EstateMixin(object):
    model = Estate
    form_class = EstateForm
    def get_success_url(self):
        return reverse('estate_list')        

class EstateCreateView(AjaxMixin, EstateMixin, CreateView):
    def get_initial(self):        
        initial = super(EstateCreateView, self).get_initial()        
        initial = initial.copy()        
        initial['estate_type'] = self.kwargs['estate_type']
        return initial
    def get_context_data(self, **kwargs):
        context = super(EstateCreateView, self).get_context_data(**kwargs)        
        context.update({
            'estate_type_name': EstateType.objects.get(pk=self.kwargs['estate_type']),
        })        
        return context

class EstateUpdateView(AjaxMixin, EstateMixin, UpdateView):
    pass

class EstateListView(TemplateView):    
    template_name = 'estate_table.html'    
    def get_context_data(self, **kwargs):
        table = EstateTable(Estate.objects.all().select_related())
        RequestConfig(self.request, paginate={"per_page": 20}).configure(table)
        context = {
            'table': table,
            'title': 'list'
        }        
        return context
    
class ClientListView(ListView):
    template_name = 'client_list.html'
    context_object_name = "clients"
    paginate_by = 10    
    def get_queryset(self):
        search_form = ClientFilterForm(self.request.GET)                
        q = Client.objects.all().select_related()
        filter_dict = search_form.get_filter()
        if len(filter_dict):
            q = q.filter(**filter_dict)        
        order_by = self.request.fields 
        if order_by:      
            return q.order_by(','.join(order_by))
        return q     
    def get_context_data(self, **kwargs): 
        context = super(ClientListView, self).get_context_data(**kwargs)       
        q = QueryDict('', mutable=True)
        q['next'] = self.request.get_full_path()
        context.update ({        
            'title': 'list',
            'next_url': q.urlencode(safe='/'),
            'client_filter_form' : ClientFilterForm(self.request.GET),
        })        
        return context

class ClientMixin(ModelFormMixin):
    model = Client
    form_class = ClientForm          
    def form_valid(self, form):
        context = self.get_context_data()
        contact_form = context['contact_formset']
        if contact_form.is_valid():
            self.object = form.save()
            contact_form.instance = self.object
            contact_form.save()
            return super(ClientMixin, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    def get_success_url(self):        
        next_url = self.request.REQUEST.get('next', '')
        if next:             
            return next_url
        return super(ClientMixin, self).get_success_url()                  

class ClientCreateView(ClientMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super(ClientCreateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : 'Добавление нового клиента'
        })            
        if self.request.POST:
            context['contact_formset'] = ContactFormSet(self.request.POST)            
        else:
            context['contact_formset'] = ContactFormSet()
        return context
      
class ClientUpdateView(ClientMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : 'Редактирование клиента «%s»' % self.object 
        })        
        if self.request.POST:
            context['contact_formset'] = ContactFormSet(self.request.POST,instance=self.object)            
        else:
            context['contact_formset'] = ContactFormSet(instance=self.object)
        return context

class ClientDeleteView(ClientMixin, DeleteView):
    template_name = 'estatebase/confirm_delete.html'
    def get_context_data(self, **kwargs):
        context = super(ClientDeleteView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление клиента...',
            'dialig_body'  : u'Подтвердите уделение клиента: %s' %  self.object    
        })
        return context    