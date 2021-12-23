from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Lead, User, Category
from .forms import LeadForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm, CategoryForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.mail import send_mail

from agents.mixins import OrganizerAndLoginRequiredMixin
# CRUD + L : Create & Retrieve & Update & Delete + List
from django.views.generic import (TemplateView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  ListView,
                                  DetailView,
                                  FormView)


# -----------------------------------------------
class SignupView(CreateView):
    model = User
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


# -----------------------------------------------
class LandingPageView(TemplateView):
    template_name = 'landing.html'


# -----------------------------------------------
class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        query_set = Lead.objects.filter(organization=user.userprofile).order_by('-id')
        if user.is_agent:
            return query_set.filter(organization=user.agent.organization).filter(agent__user=user)
        return query_set

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            query_set = Lead.objects.filter(organization=user.userprofile, agent__isnull=True)
            context.update({
                'unassigned_leads': query_set
            })
        return context


# -----------------------------------------------
class LeadDetailView(LoginRequiredMixin, DetailView):
    # model = Lead
    # queryset = Lead.objects.all()
    context_object_name = 'lead'
    template_name = 'leads/lead_detail.html'

    def get_queryset(self):
        user = self.request.user
        query_set = Lead.objects.filter(organization=user.userprofile)
        if user.is_agent:
            return query_set.filter(organization=user.agent.organization).filter(agent__user=user)
        return query_set


# -----------------------------------------------
class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    model = Lead
    form_class = LeadForm

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        send_mail(
            subject='A lead has been created',
            message='Go to the site to see the new lead',
            from_email='test@test.com',
            recipient_list=['test2@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)


# -----------------------------------------------
class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    # model = Lead
    form_class = LeadForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('leads:lead-detail', args=[pk])

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)


# -----------------------------------------------
class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    template_name = 'leads/lead_delete_confirm.html'

    def get_success_url(self):
        return reverse('leads:lead-list')

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)


# -----------------------------------------------
class AssignAgentView(OrganizerAndLoginRequiredMixin, FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = get_object_or_404(Lead, id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


# -----------------------------------------------
class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryListView, self).get_context_data(**kwargs)
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        context.update({
            'unassigned_lead_count': queryset.filter(organization__agent__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            return Category.objects.filter(organization=user.userprofile).order_by('-id')
        else:
            return Category.objects.filter(organization=user.agent.organization).order_by('-id')


# ----------------------------------------------------
class CategoryCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organization = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


# -----------------------------------------------
class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)

        # get_object() fetch that specific object which we are using in Detail view
        # leads = Lead.objects.filter(category=self.get_object())
        # or
        # because we have ForeignKey from lead to category model
        # leads = self.get_object().lead_set.all()
        # because we gave related name to category foreignkey field in Lead model
        leads = self.get_object().leads.all()

        context.update({
            'leads': leads
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            return Category.objects.filter(organization=user.userprofile)
        else:
            return Category.objects.filter(organization=user.agent.organization)


# ----------------------------------------------------------
class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryUpdateForm
    context_object_name = 'lead'

    def get_success_url(self):
        pk = self.get_object().id
        return reverse('leads:lead-detail', kwargs={'pk': pk})

    def get_queryset(self):
        user = self.request.user
        if user.is_agent:
            return Lead.objects.filter(
                organization=user.agent.organization).filter(agent__user=user)
        return Lead.objects.filter(organization=user.userprofile)

# -------------------------------------------------------------------------------
# Function Base Views -----------------------------------------------------------
# def landing_page(request):
#     return render(request, 'landing.html')
#
#
# def lead_list(request):
#     leads = Lead.objects.all().order_by('-id')
#     return render(request, 'leads/lead_list.html', context={'leads': leads})
#
#
# def lead_detail(request, pk):
#     lead = Lead.objects.get(id=pk)
#     return render(request, 'leads/lead_detail.html', context={'lead': lead})
#
#
# def lead_create(request):
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             lead = form.save()
#             return HttpResponseRedirect(reverse('leads:lead-detail', args=[lead.id]))
#
#     form = LeadForm()
#     return render(request, 'leads/lead_create.html', context={'form': form})
#
#
# def lead_update(request, pk):
#     lead = get_object_or_404(Lead, pk=pk)
#     form = LeadForm(request.POST or None, instance=lead)
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect(reverse('leads:lead-detail', args=[lead.id]))
#     return render(request, 'leads/lead_update.html',
#                   context={'form': form, 'lead': lead})
#
#
# def lead_delete(request, pk):
#     lead = get_object_or_404(Lead, pk=pk)
#     if request.method == "POST":
#         lead.delete()
#         return redirect('leads:lead-list')
#     return render(request, 'leads/lead_delete_confirm.html', {'lead': lead})
