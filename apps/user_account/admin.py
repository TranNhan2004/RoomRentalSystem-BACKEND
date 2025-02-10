from django.contrib import admin
from django import forms
from .models import CustomUser


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if kwargs.get('instance') and kwargs['instance'].id is not None:
            if 'role' in self.fields:
                self.fields['role'].widget.attrs['readonly'] = 'readonly'
                self.fields['role'].widget.attrs['disabled'] = 'disabled'
        else:
            if 'role' in self.fields:
                choices = list(self.fields['role'].choices)
                choices = [choice for choice in choices if choice[0] != 'A'] 
                self.fields['role'].choices = choices

class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
    list_display = [field.name for field in CustomUser._meta.fields]

admin.site.register(CustomUser, CustomUserAdmin)