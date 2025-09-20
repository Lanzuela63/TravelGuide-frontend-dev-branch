from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (
    Province, CityMunicipality, Barangay,
    TouristSpot, Hotel, Restaurant,
    Category, CategorizedItem,
    Review, Gallery, OperatingHour,
    SavedSpot, VisitedSpot
)
from django import forms


# --- GENERIC INLINE CONFIGURATIONS --- #
class ReviewInline(GenericTabularInline):
    model = Review
    extra = 0
    fields = ("user", "rating", "star_display", "comment", "created_at")
    readonly_fields = ("star_display", "created_at")

    def star_display(self, obj):
        if not obj.rating:
            return "No rating"
        stars = "★" * obj.rating + "☆" * (5 - obj.rating)
        return stars

    star_display.short_description = "Stars"


class GalleryInline(GenericTabularInline):
    model = Gallery
    extra = 1


class OperatingHourInline(GenericTabularInline):
    model = OperatingHour
    extra = 1


# --- FORMS --- #
class BaseLocationForm(forms.ModelForm):
    province = forms.ModelChoiceField(queryset=Province.objects.all(), required=False)
    
    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial queryset for city and barangay based on existing object
        if self.instance.pk:
            if self.instance.province:
                self.fields['city'].queryset = CityMunicipality.objects.filter(province=self.instance.province)
            if self.instance.city:
                self.fields['barangay'].queryset = Barangay.objects.filter(city=self.instance.city)
        else:
            # For new objects, initially show no cities/barangays
            self.fields['city'].queryset = CityMunicipality.objects.none()
            self.fields['barangay'].queryset = Barangay.objects.none()


class TouristSpotForm(BaseLocationForm):
    class Meta(BaseLocationForm.Meta):
        model = TouristSpot

class HotelForm(BaseLocationForm):
    class Meta(BaseLocationForm.Meta):
        model = Hotel

class RestaurantForm(BaseLocationForm):
    class Meta(BaseLocationForm.Meta):
        model = Restaurant


# --- MAIN MODELS --- #
@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", "psgc_code")
    search_fields = ("name", "psgc_code")


@admin.register(CityMunicipality)
class CityMunicipalityAdmin(admin.ModelAdmin):
    list_display = ("name", "psgc_code", "province")
    list_filter = ("province",)
    search_fields = ("name", "psgc_code")


@admin.register(Barangay)
class BarangayAdmin(admin.ModelAdmin):
    list_display = ("name", "psgc_code", "city")
    list_filter = ("city__province", "city")
    search_fields = ("name", "psgc_code")


@admin.register(TouristSpot)
class TouristSpotAdmin(admin.ModelAdmin):
    form = TouristSpotForm
    list_display = ("name", "city", "is_featured", "is_active", "show_in_carousel", "average_rating")
    list_editable = ("show_in_carousel",)
    search_fields = ("name", "description")
    list_filter = ("is_featured", "is_active", "show_in_carousel", "city__province")
    inlines = [ReviewInline, GalleryInline, OperatingHourInline]
    change_form_template = 'admin/tourism/change_form.html'


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    form = HotelForm
    list_display = ("name", "city", "stars", "is_active", "is_featured", "average_rating")
    search_fields = ("name", "amenities")
    list_filter = ("stars", "city__province")
    inlines = [ReviewInline, GalleryInline, OperatingHourInline]
    change_form_template = 'admin/tourism/change_form.html'


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    form = RestaurantForm
    list_display = ("name", "city", "cuisine_type", "is_active", "is_featured", "average_rating")
    search_fields = ("name", "cuisine_type")
    list_filter = ("city__province",)
    inlines = [ReviewInline, GalleryInline, OperatingHourInline]
    change_form_template = 'admin/tourism/change_form.html'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(CategorizedItem)
class CategorizedItemAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "content_type", "object_id")
    search_fields = ("category__name",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "rating", "created_at", "content_type", "object_id")
    list_filter = ("rating", "created_at", "content_type")
    search_fields = ("user__username", "comment")
    ordering = ("-created_at",)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "content_type", "object_id", "caption")
    search_fields = ("caption",)


@admin.register(OperatingHour)
class OperatingHourAdmin(admin.ModelAdmin):
    list_display = ("id", "content_type", "object_id", "day_of_week", "open_time", "close_time")
    list_filter = ("day_of_week",)


@admin.register(SavedSpot)
class SavedSpotAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "spot", "saved_at")
    search_fields = ("user__username", "spot__name")
    list_filter = ("saved_at",)


@admin.register(VisitedSpot)
class VisitedSpotAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "spot", "visited_at")
    search_fields = ("user__username", "spot__name")
    list_filter = ("visited_at",)


# Optional: Customize Admin Site Branding
admin.site.site_header = "Bicol Travel Guide Admin"
admin.site.site_title = "Bicol Travel CMS"
admin.site.index_title = "Welcome to the Bicol Travel Admin Portal"