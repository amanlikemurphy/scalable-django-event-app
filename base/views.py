from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Event, Registration
from .forms import RegistrationForm, CustomUserCreateForm, EventForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

#function for homepage.
def home_page(request): 
    events = Event.objects.all()
    categories = Event.objects.values_list('category', flat=True).distinct()
    context = {'events':events, 'categories': categories}
    return render(request, 'home.html', context)

#function to view an event.
def event_page(request, pk):
    event =  Event.objects.get(id=pk)
    num_attending = Registration.objects.filter(event=event).count()
    context = {'event': event, 'num_attending': num_attending}
    return render(request, 'event.html', context)


def event_category(request, category):
    events = Event.objects.filter(category=category)
    return render(request, 'event_category.html', {'events': events, 'category': category})

 
#function to register for an event.
@login_required()
def attend_page(request, pk):
    event = Event.objects.get(id=pk)
    user = request.user
    registration_exists = Registration.objects.filter(user=request.user, event=event).exists()

    if registration_exists:
        # If a registration already exists, redirect to the event page
        messages.warning(request, 'You have already registered for this event.')
        return redirect('event', pk=event.id)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.event = event
            registration.save()
            messages.success(request, 'You have successfully registered for this event!')
            event.attendees.add(request.user)
            return redirect('event', pk=event.id)
        
    else:
        form = RegistrationForm()
    
    context = {'event':event, 'form':form, 'registration_exists':registration_exists}
    return render(request, 'attend_event.html', context)

#function to create user's profile.
def user_page(request, pk):
    user = User.objects.get(id=pk)
    context = {'user':user}
    return render(request, 'profile.html', context)

#function to create account's page.
@login_required(login_url ='/login')
def account_page(request, pk):
    user = request.user
    created_events = Event.objects.filter(creator=user)
    context = {'user':user, 'created_events': created_events,}
    return render(request, 'account.html', context)


#function to login to account.
def login_page(request):
    page = 'login'

    if request.method == "POST":
        user = authenticate(
            email=request.POST['email'],
            password=request.POST['password']
            )
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
    context = {'page':page}
    return render(request, 'login_register.html', context)

#function to logout from account.
def logout_user(request):
    logout(request)
    return redirect('login')


#function to sign up as a user.
def register_page(request):
    form = CustomUserCreateForm()
    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user) 
            return redirect('home')
    page = 'register'
    context = {'page':page, 'form':form}
    return render(request, 'login_register.html', context)

#function to create an event.
@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            '''
            if 'featured_image' in request.FILES:
                event.featured_image = request.FILES['featured_image']
                '''
            event.save()
            return redirect('event', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'event_create.html', {'form': form})

#function to display the events that a user has registered for.
def registrations_page(request):
    registrations = Registration.objects.filter(user=request.user)
    context = {'registrations': registrations}
    return render(request, 'registrations.html', context)

#function to edit events.
@login_required()
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.creator:
        # If the user is not the creator of the event, unauthorize and redirect to the event page
        messages.error(request, 'You are not authorized to edit this event.')
        return redirect('event', event=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            # Set the creator field of the event instance
            event = form.save(commit=False)
            event.creator = request.user
            '''
            if 'featured_image' in request.FILES:
                event.featured_image = request.FILES['featured_image']
            '''
            event.save()
            messages.success(request, 'Event updated successfully.')
            return redirect(reverse('event', args=[event.pk]))
    else:
        form = EventForm(instance=event)
    context = {'form': form, 'event': event}
    return render(request, 'edit_event.html', context)

#function to delete an event
@login_required()
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.creator:
        # If the user is not the creator of the event, unauthorize and redirect to the event page
        messages.error(request, 'You are not authorized to edit this event.')
        return redirect('event', pk=event.pk)
    
    if request.method == 'POST':
        event.delete()
        return redirect(reverse('account', args=[request.user.pk]))
    
    context = {'event': event}
    return render(request, 'delete_event.html', context)


#function to search for events
def search(request):
    query = request.GET.get('query')
    events = Event.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'events': events, 'query': query})







