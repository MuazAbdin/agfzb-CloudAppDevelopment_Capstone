from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.
class CarModelInline(admin.StackedInline):
  model = CarModel
  extra = 3

class CarModelAdmin(admin.ModelAdmin):
  list_display = ('dealer_id', 'type', 'get_maker','name', 'year')
  list_filter = ['dealer_id','type', 'year']
  search_fields = ['dealer_id', 'type', 'get_maker','name', 'year']
  
  def get_maker(self, obj):
    return obj.car_make.name
  get_maker.admin_order_field = 'car_make'
  get_maker.short_description = 'Car Maker'
  

class CarMakeAdmin(admin.ModelAdmin):
  inlines =  [CarModelInline]
  list_display = ('name','description')
  list_filter = ['name']
  search_fields = ['name']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
