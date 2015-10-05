from django.shortcuts import render
from django.views.generic import TemplateView

from blockchain.models import Block

# Create your views here.

class DefaultView(TemplateView):
    template_name = 'default.html'

    def get_context_data(self, **kwargs):
        ctx = super(DefaultView, self).get_context_data(**kwargs)
        ctx['blocks'] = Block.objects.all()
        return ctx