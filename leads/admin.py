from django.contrib import admin
from .models import Lead, Agent, User, UserProfile, Category


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    class Meta:
        model = Lead
        fields = '__all__'


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    class Meta:
        model = Agent
        fields = '__all__'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category
        fields = '__all__'
