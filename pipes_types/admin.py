from django import forms
from django.contrib import admin

from .models import PipeColor, PipeDiameter, PipeType, PipeMark, PipeLeftEnd, PipeRightEnd, PipeOutflow
# Register your models here.


class PipeColorAdmin(admin.ModelAdmin):

    list_display = ('name', 'available')
    list_filter = ('available',)
    search_fields = ('name',)
    ordering = ('name',)


class PipeDiameterAdmin(admin.ModelAdmin):

    list_display = ('name', 'available')
    list_filter = ('available',)
    search_fields = ('name',)
    ordering = ('name',)


class PipeTypeAdmin(admin.ModelAdmin):

    list_display = ('name', 'available')
    list_filter = ('available',)
    search_fields = ('name',)
    ordering = ('name',)


class PipeMarkAdmin(admin.ModelAdmin):

    list_display = ('name', 'available')
    list_filter = ('available',)
    search_fields = ('name',)
    ordering = ('name',)


class PipeEndAdmin(admin.ModelAdmin):

    list_display = ('name', 'available')
    list_filter = ('available',)
    search_fields = ('name',)
    ordering = ('name',)


class PipeOutflowAdmin(admin.ModelAdmin):

    list_display = ('name', 'available')
    list_filter = ('available',)
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(PipeColor, PipeColorAdmin)
admin.site.register(PipeDiameter, PipeDiameterAdmin)
admin.site.register(PipeType, PipeDiameterAdmin)
admin.site.register(PipeMark, PipeMarkAdmin)
admin.site.register(PipeLeftEnd, PipeEndAdmin)
admin.site.register(PipeRightEnd, PipeEndAdmin)
admin.site.register(PipeOutflow, PipeOutflowAdmin)