# My Django imports
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from pprint import pprint

# My app imports
from PAS_assessment.decorator import validate_department
from PAS_auth.views import SPLIT

from PAS_auth.models import (
    Programme,
    StudentProfile,
    Allocate,
)
from PAS_hallAllocation.models import (
    Venue,
    StudHallAllocation,
    AssessorHallAllocation,
    DaysOfDefense,
)

from PAS_hallAllocation.form import (
    VenueForm,
    DefenseDaysForm,
    EditDefenseDaysForm,
    StudHallAllocationForm,
    RStudHallAllocationForm,
    MStudHallAllocationForm,
    AssessHallAllocationForm,
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
class UDVenuesView(LoginRequiredMixin, View):
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
            if 'edit' in request.POST:
                form = VenueForm(request.POST, instance=venue)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Venue Edited Successfully!')
                    return redirect('hall:venues', dept_id.pk)

            elif 'delete' in request.POST:
                venue.delete()
                messages.success(request, 'Venue Deleted Successfully!')
                return redirect('hall:venues', dept_id.pk)

            messages.error(request, 'failed to process request!')
            venues = Venue.objects.all()

            return render(request, 'hall/venues.html', context={'dept':dept_id, 'form':form, 'venues':venues, 'type':self.view_type})
        else:
            messages.error(request, 'Unable to fetch venue!')

        venues = Venue.objects.all()
        return render(request, 'hall/venues.html', context={'dept':dept_id, 'form':form, 'venues':venues, 'type':self.view_type})

@method_decorator(validate_department, name="get")
@method_decorator(validate_department, name="post")
class DefenseDaysView(LoginRequiredMixin, View):
    form = DefenseDaysForm()
    view_type = 'create'

    def get(self, request, dept_id):
        days = DaysOfDefense.objects.all().order_by('-date_created')
        return render(request, 'hall/defense_day.html', context={'dept':dept_id, 'form':self.form, 'days':days, 'type':self.view_type})

    def post(self, request, dept_id):
        days = DaysOfDefense.objects.all().order_by('-date_created')
        form = DefenseDaysForm(request.POST, dept_id=dept_id.pk)

        if form.is_valid():
            to_save = form.save(commit=False)
            to_save.dept_id = dept_id
            to_save.save()
            messages.success(request, 'Defense Days Created Successfully!')
            return redirect('hall:defense_days', dept_id.pk)

        return render(request, 'hall/defense_day.html', context={'dept':dept_id, 'form':form, 'days':days, 'type':self.view_type})

@method_decorator(validate_department, name="get")
@method_decorator(validate_department, name="post")
class UDDefenseDaysView(LoginRequiredMixin, View):
    view_type = 'edit'
    def get_days(self, dept_id, day_id):
        try:
            return DaysOfDefense.objects.get(days_id=day_id, dept_id=dept_id)
        except ObjectDoesNotExist: pass
        except ValidationError: pass
        return None

    def get(self, request, dept_id, day_id):
        day = self.get_days(dept_id, day_id)

        if day:
            form = DefenseDaysForm(instance=day, dept_id=dept_id)
            days = DaysOfDefense.objects.all().order_by('-date_created')
            return render(request, 'hall/defense_day.html', context={'dept':dept_id, 'form':form, 'days':days, 'type':self.view_type})
        else:
            messages.error(request, 'Unable to edit day of defense!')
            return redirect('hall:defense_days', dept_id.pk)

    def post(self, request, dept_id, day_id):
        day = self.get_days(dept_id, day_id)

        if day:
            form = EditDefenseDaysForm(request.POST, instance=day, dept_id=dept_id)

            if 'edit' in request.POST:
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Day of defense edited successfully!')
                    return redirect('hall:defense_days', dept_id.pk)

            elif 'delete' in request.POST:
                day.delete()
                messages.success(request, 'Day of defense deleted successfully!')
                return redirect('hall:defense_days', dept_id.pk)

            messages.error(request, 'failed to process request!')
            days = DaysOfDefense.objects.all()

            return render(request, 'hall/defense_day.html', context={'dept':dept_id, 'form':form, 'days':days, 'type':self.view_type})
        else:
            messages.error(request, 'Unable to fetch day of defense!')

        days = DaysOfDefense.objects.all()
        return render(request, 'hall/defense_day.html', context={'dept':dept_id, 'form':form, 'days':days, 'type':self.view_type})

@method_decorator(validate_department, name="get")
@method_decorator(validate_department, name="post")
class CRStudentHallAllocationView(LoginRequiredMixin, View):
    view_type = 'create'

    def get(self, request, dept_id):
        form = StudHallAllocationForm(dept_id=dept_id)
        form2 = MStudHallAllocationForm(dept_id=dept_id)
        return render(request, 'hall/student_to_hall.html', context={'dept':dept_id, 'form':form, 'form2':form2, 'type':self.view_type})

    def post(self, request, dept_id):
        if 'authA' in request.POST:
            # CHECK IF VENUE AND STUDENTS EXISTS

            form = StudHallAllocationForm(request.POST, dept_id=dept_id)
            form2 = MStudHallAllocationForm(request.POST, dept_id=dept_id)

            if form.is_valid():

                prog_id = form.cleaned_data.get('prog_id')
                sess_id = form.cleaned_data.get('sess_id')
                type_id = form.cleaned_data.get('type_id')

                allocation = {}

                # TRY TO GET DEFENSE DAYS
                try:
                    match_days = DaysOfDefense.objects.get(prog_id=prog_id, sess_id=sess_id, dept_id=dept_id, type_id=type_id)
                except ObjectDoesNotExist:
                    messages.error(request, 'Days of defense not set, SET days first!!')
                else:
                    # GET ALL STUDENTS WITH THE REQUEST PARAMETERS
                    match_studs_list = list(Allocate.objects.filter(type_id=type_id, dept_id=dept_id, sess_id=sess_id, prog_id=prog_id))

                    match_venue_list = list(Venue.objects.filter(prog_id=prog_id))
                    index = 1
                    days = 1
                    objs = []

                    if match_studs_list and match_venue_list:

                        # CREATING A DICT OF VENUE
                        for i in range(len(match_venue_list)):
                            allocation[match_venue_list[i]] = []

                        if prog_id.programme_title == 'HND':

                            # ASSIGN STUDENTS TO HALL
                            while match_studs_list:
                                for i in match_studs_list:
                                    if index <= len(match_venue_list):
                                        allocation[match_venue_list[index - 1]].insert(0, match_studs_list.pop())
                                    else:
                                        index = 1
                                        allocation[match_venue_list[index - 1]].insert(0, match_studs_list.pop())
                                    index += 1

                            # PREPARE OBJECTS FOR BATCH CREATE
                            for (key, value) in allocation.items():
                                for v in value:
                                    objs.append(StudHallAllocation(venue_id=key, prog_id=prog_id, sess_id=sess_id, dept_id=dept_id, type_id=type_id, stud_id=v.stud_id, day_num=days))
                                    days += 1
                                    if days > match_days.num_of_day:
                                        days = 1
                                days = 1

                        elif prog_id.programme_title == 'ND':
                            # get a student from student list
                            while match_studs_list:
                                for stud in match_studs_list:
                                    # Filter allocation to get group members
                                    stud_group_members = Allocate.objects.filter(group_id=stud.group_id, type_id=type_id, dept_id=dept_id, sess_id=sess_id, prog_id=prog_id)

                                    # ASSIGN STUDENTS TO HALL
                                    def _allocate_nd():
                                        for member in stud_group_members:
                                            objs.append(StudHallAllocation(venue_id=match_venue_list[index - 1], prog_id=prog_id, sess_id=sess_id, dept_id=dept_id, type_id=type_id, stud_id=member.stud_id, day_num=days))
                                            match_studs_list.remove(member)

                                    if index <= len(match_venue_list):
                                        if days <= match_days.num_of_day:
                                            _allocate_nd()
                                        else:
                                            days = 1
                                            _allocate_nd()
                                    else:
                                        index = 1
                                        if days <= match_days.num_of_day:
                                            _allocate_nd()
                                        else:
                                            days = 1
                                            _allocate_nd()

                                    index += 1
                                    days += 1

                        # SAVE RECORD TO TABLE: -> ALLOCATE
                        allocations = StudHallAllocation.objects.bulk_create(objs)

                        # DISPLAY THE ALLOCATION
                        groupings = ManageHallAllocationView().retrieve(prog_id, sess_id, type_id, dept_id.pk)

                        return render(request, 'hall/student_to_hall.html', context={'dept':dept_id, 'form':form, 'form2':form2, 'type':self.view_type, 'groupings':groupings})

                    else:
                        if not match_studs_list:
                            messages.error(request, 'No student found with the supplied information!')

                        if not match_venue_list:
                            messages.error(request, 'No Venue found! try adding defense venues')

            return render(request, 'hall/student_to_hall.html', context={'dept':dept_id, 'form':form, 'form2':form2, 'type':self.view_type})

        elif 'mAllocate' in request.POST:
            form = StudHallAllocationForm(dept_id=dept_id)
            form2 = MStudHallAllocationForm(request.POST, dept_id=dept_id)

            if form2.is_valid():
                data = form2.save(commit=False)
                user = form2.cleaned_data.get('stud_id')
                data.sess_id = user.session_id
                data.dept_id = user.dept_id
                data.prog_id = user.programme_id
                data.type_id = user.type_id

                messages.success(request, f'{user.user_id.get_fullname()} has been allocated!')
                data.save()
                return redirect('hall:manage_hall_allocation', dept_id.pk)

            messages.error(request, f'{form2.errors.as_text()}')
            return render(request, 'hall/student_to_hall.html', context={'dept':dept_id, 'form':form, 'form2':form2, 'type':self.view_type})

@method_decorator(validate_department, name="get")
@method_decorator(validate_department, name="post")
class ManageHallAllocationView(LoginRequiredMixin, View):

    def retrieve(self, prog_id, sess_id, type_id, dept_id):
        hall_allocation = StudHallAllocation.objects.filter(prog_id=prog_id, sess_id=sess_id, type_id=type_id, dept_id=dept_id)

        """
            check = [
                ['HND1',
                    ['Day 1',
                        ['CST20HND0406',
                         'CST20HND0406',
                         'CST20HND0406']
                        ],

                    ['Day 2',
                        ['CST20HND0406',
                         'CST20HND0406',
                         'CST20HND0406']],
                    ['Day 3', ['CST20HND0406', 'CST20HND0406', 'CST20HND0406']],
                ],
                ['Odfel', ['Day 1', ['CST20HND0406', 'CST20HND0406', 'CST20HND0406']], ['Day 2', ['CST20HND0406', 'CST20HND0406', 'CST20HND0406']],  ['Day 3', ['CST20HND0406', 'CST20HND0406', 'CST20HND0406']],
                ],
            ]
        """

        groupings = []

        for allocation in hall_allocation:

            if not groupings:
                groupings.append([allocation.venue_id, [allocation.day_num, [allocation.stud_id]]])
            else:
                for group in groupings:
                    if allocation.venue_id in group:
                        for i in range(1, len(group)):
                            if allocation.day_num in group[i]:
                                group[i][1].append(allocation.stud_id)
                                break
                        else:
                            group.append([allocation.day_num, [allocation.stud_id]])
                            break
                        break
                else:
                    groupings.append([allocation.venue_id, [allocation.day_num, [allocation.stud_id]]])

        return groupings

    def get(self, request, dept_id):
        form = RStudHallAllocationForm(dept_id=dept_id)

        return render(request, 'hall/manage_hall_allocation.html', context={'dept':dept_id, 'form':form})

    def post(self, request, dept_id):
        form = RStudHallAllocationForm(request.POST, dept_id=dept_id)
        if form.is_valid():

            prog_id = form.cleaned_data.get('prog_id')
            sess_id = form.cleaned_data.get('sess_id')
            type_id = form.cleaned_data.get('type_id')

            groupings = self.retrieve(prog_id, sess_id, type_id, dept_id)

            return render(request, 'hall/manage_hall_allocation.html', context={'dept':dept_id, 'form':form, 'groupings':groupings})
        print(form.errors)

        return render(request, 'hall/manage_hall_allocation.html', context={'dept':dept_id, 'form':form})


@method_decorator(validate_department, name="get")
@method_decorator(validate_department, name="post")
class CRAssessorHallAllocationView(LoginRequiredMixin, View):
    view_type = 'allocate'

    def get(self, request, dept_id):
        form = AssessHallAllocationForm(dept_id=dept_id)
        allocations = AssessorHallAllocation.objects.all()
        return render(request, 'hall/assessor_to_hall.html', context={'dept':dept_id, 'form':form, 'type':self.view_type, 'allocations':allocations})

    def post(self, request, dept_id):
        form = AssessHallAllocationForm(request.POST, dept_id=dept_id)
        allocations = AssessorHallAllocation.objects.all()

        if form.is_valid():
            data = form.save(commit=False)
            data.dept_id = dept_id
            data.save()
            messages.success(request, 'Allocation of accessor to venue, successful')
            return redirect('hall:cr_assessor_hall', dept_id.pk)

        messages.error(request, 'Failed in allocating accessor to venue')
        return render(request, 'hall/assessor_to_hall.html', context={'dept':dept_id, 'form':form, 'type':self.view_type, 'allocations':allocations})