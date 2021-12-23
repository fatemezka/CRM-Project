import random

from django.core.mail import send_mail

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse

from leads.models import *
from .forms import AgentForm
from .mixins import OrganizerAndLoginRequiredMixin


# LIST
class AgentListView(OrganizerAndLoginRequiredMixin, ListView):
    template_name = 'agents/agent_list.html'
    # model = Agent
    context_object_name = 'agents'

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile).order_by('-id')


# CREATE
class AgentCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        # commit = False : it does not save this form directly to the database
        # before our job
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0, 1000000)}")  # just a random password
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.userprofile
        )
        send_mail(
            subject='You are invited to be an agent',
            message='You were added as an agent on CRM Project. please come login to start working.',
            from_email='admin@test.com',  # email sender
            recipient_list=[user.email]  # email receiver
        )
        return super(AgentCreateView, self).form_valid(form)


# DETAIL
class AgentDetailView(OrganizerAndLoginRequiredMixin, DetailView):
    # model = Agent
    context_object_name = 'agent'
    template_name = 'agents/agent_detail.html'

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile)


# UPDATE
class AgentUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    # model = Agent
    template_name = 'agents/agent_update.html'
    form_class = AgentForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('agents:agent-detail', args=[pk])

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organization = self.request.user.userprofile
        agent.save()
        return super(AgentUpdateView, self).form_valid(form)

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile)


# DELETE
class AgentDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    # model = Agent
    template_name = 'agents/agent_confirm_delete.html'

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile)
