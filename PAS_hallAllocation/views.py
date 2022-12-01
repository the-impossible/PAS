# My Django imports
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

# My app imports
from PAS_assessment.decorator import validate_department

from PAS_auth.models import (
    Programme,
)
from PAS_hallAllocation.models import (
    Venue,
    StudHallAllocation,
    AssessorHallAllocation,
)

from PAS_hallAllocation.form import (
    VenueForm,
)

# Create your views here.
@method_decorator(validate_department, name="get")
class HallAllocationDashboardView(LoginRequiredMixin, View):

    def get(self, request, dept_id):
        programmes = Programme.objects.all()

        return render(request, 'hall/hall_dashboard.html', context={'dept':dept_id, 'programmes':programmes})

@method_decorator(validate_department, name="get")
@method_decorator(validate_department, name="post")
class VenuesView(LoginRequiredMixin, View):
    form = VenueForm()
    view_type = 'create'

    def get(self, request, dept_id):
        venues = Venue.objects.all().order_by('-date_created')
        return render(request, 'hall/venues.html', context={'dept':dept_id, 'form':self.form, 'venues':venues, 'type':self.view_type})

    def post(self, request, dept_id):
        venues = Venue.objects.all().order_by('-date_created')
        form = VenueForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Venue Created Successfully!')
            return redirect('hall:venues', dept_id.pk)

        return render(request, 'hall/venues.html', context={'dept':dept_id, 'form':self.form, 'venues':venues, 'type':self.view_type})


@method_decorator(validate_department, name="get")
@method_decorator(validate_department, name="post")
class EditVenuesView(LoginRequiredMixin, View):
    view_type = 'edit'
    def get_venue(self, venue_id, dept_id):
        try:
            venue = Venue.objects.get(venue_id=venue_id)
            return Venue.objects.get(venue_id=venue_id)
        except ObjectDoesNotExist: pass
        except ValidationError: pass
        return None

    def get(self, request, dept_id, venue_id):
        venue = self.get_venue(venue_id, dept_id)

        if venue:
            form = VenueForm(instance=venue)
            venues = Venue.objects.all().order_by('-date_created')
            return render(request, 'hall/venues.html', context={'dept':dept_id, 'form':form, 'venues':venues, 'type':self.view_type})
        else:
            messages.error(request, 'Unable to Edit venue!')
            return redirect('hall:venues', dept_id.pk)

    def post(self, request, dept_id, venue_id):
        venue = self.get_venue(venue_id, dept_id)

        if venue:
            form = VenueForm(request.POST, instance=venue)
            if form.is_valid():
                form.save()
                messages.success(request, 'Venue Edited Successfully!')
                return redirect('hall:venues', dept_id.pk)

        messages.error(request, 'Unable to Edit venue!')
        venues = Venue.objects.all()
        return render(request, 'hall/venues.html', context={'dept':dept_id, 'form':form, 'venues':venues, 'type':self.view_type})

@method_decorator(validate_department, name="post")
class DeleteVenuesView(LoginRequiredMixin, View):
    view_type = 'create'
    def get_venue(self, venue_id, dept_id):
        try:
            venue = Venue.objects.get(venue_id=venue_id)
            return Venue.objects.get(venue_id=venue_id)
        except ObjectDoesNotExist: pass
        except ValidationError: pass
        return None

    def post(self, request, dept_id, venue_id):
        venue = self.get_venue(venue_id, dept_id)
        if venue:
            venue.delete()
            messages.success(request, 'Venue Deleted Successfully!')
            return redirect('hall:venues', dept_id.pk)

        venues = Venue.objects.all()
        messages.error(request, 'Unable to Delete venue!')
        return render(request, 'hall/venues.html', context={'dept':dept_id, 'form':form, 'venues':venues, 'type':self.view_type})
