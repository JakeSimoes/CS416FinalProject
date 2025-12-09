from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from .models import Event, Post
from .forms import EventForm, PostForm
import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import time

# Create your views here.

def home(request):
    context = {}
    if request.method == "GET":
        genre = request.GET.get("genre", None)
        city = request.GET.get("city", None)
        toast = request.GET.get("toast", None)
        if toast:
            context.update({"toast": toast})
        if request.user:
            context.update({"user": request.user})
        # If you're missing either parameter, you're ignored
        if genre and city:
            # The user is giving us a valid request
            events_data, count = get_event_info(request)
            context.update({"events_data": events_data,
                       "genre": genre,
                       "city": city,
                       "count": count,
                       "display": True})

    # The user has just landed on the page
    return render(request, 'home.html', context)

def view_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    feedback = None
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            # Yes I know this can be done automatically if I keep the form instance above, but formatting that instance is annoying
            feedback = "Invalid username or password"

    context = {"form": AuthenticationForm(), "feedback": feedback}
    return render(request, 'login.html', context)

def view_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def view_register(request):
    form = None
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # This whole dance is for getting a successful registration toast to appear after being redirected home
            base_url = reverse('home')
            query_string = urlencode({'toast': 'registerSuccess'})
            return redirect(f'{base_url}?{query_string}')

    # The user has just landed on the page
    context = {"form": form or UserCreationForm()}
    return render(request, 'register.html', context)

def view_discuss(request, discussion_id):
    # It'd be neat to do everything through this one endpoint using PUT and DELETE requests
    # But that'd take too much time
    if request.method == "POST":
        # If the user is posting, check that they're authenticated, and save a new post
        if request.user.is_authenticated:
            new_post = Post.objects.create(user=request.user, event=Event.objects.get(id=discussion_id), text_content=request.POST.get("post_text", None))
            new_post.save()
        return redirect("discuss", discussion_id=discussion_id)
    if request.method == "GET":
        try:
            # If the user is getting, try to get the discussion ID they want, if that fails, send them home
            event = Event.objects.get(id=discussion_id)
            context = {"event": event, "posts": event.post_set.all()}
            return render(request, 'discuss.html', context)
        except ObjectDoesNotExist:
            redirect('home')

def view_discuss_create(request):
    # Perhaps not the most secure, a user can technically make up any event they want
    if request.method == "POST":
        form = EventForm(request.POST)
        # If a discussion already exists for this event, send them to it
        existing_events = Event.objects.filter(ticketmaster_id=request.POST.get("ticketmaster_id", None))
        if existing_events:
            return redirect("discuss", discussion_id=existing_events[0].id)
        # Otherwise start a new discussion
        elif form.is_valid() and request.user.is_authenticated:
            new_event = form.save()
            return redirect("discuss", discussion_id=new_event.id)

    return redirect('home')

def view_discuss_delete(request):
    # Allows a user to delete a post (given it's their post or if they're an admin)
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        discussion_id = post.event.id
        if request.user.is_authenticated and (request.user == post.user or request.user.is_staff):
            post.delete()
        return redirect('discuss', discussion_id=discussion_id)
    else:
        return redirect('home')

def view_discuss_update(request):
    # Allows a user to edit a post (given it's their post)
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        new_text_content = request.POST.get("text_content")
        post = Post.objects.get(id=post_id)
        discussion_id = post.event.id
        if request.user.is_authenticated and post.user == request.user:
            post.text_content = new_text_content
            post.save()
        return redirect("discuss", discussion_id=discussion_id)
    else:
        return redirect('home')

def get_event_info(request):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    genre = request.GET["genre"]
    city = request.GET["city"]

    parameters = {
        'classificationName': genre,
        'city': city,
        'sort': "date,asc",
        'apikey': "zSmOKgJcKkKgW73hoU3Q3AwStOWECZGf",
    }

    raw_response = requests.get(url, params=parameters)
    response = raw_response.json()
    if raw_response.status_code == requests.codes.ok:
        events = []
        # Doing this here cause apparently Django can't handle underscores in templates
        if not "_embedded" in response:
            return [], []
        for event in response["_embedded"]['events']:
            temp_dict = {}
            temp_dict["img_url"] = image_selector(event["images"])["url"]
            temp_dict["name"] = event["name"]
            temp_dict["venue"] = event["_embedded"]["venues"][0]["name"]
            temp_dict["address"] = event["_embedded"]["venues"][0]["address"]["line1"]
            temp_dict["city"] = event["_embedded"]["venues"][0]["city"]["name"]
            temp_dict["state"] = event["_embedded"]["venues"][0]["state"]["name"]
            temp_dict["url"] = event["url"]
            if "dateTime" in event["dates"]["start"]:
                event_time = datetime.fromisoformat(event["dates"]["start"]["dateTime"]).astimezone(ZoneInfo("America/New_York"))
                temp_dict["datetime"] = event["dates"]["start"]["dateTime"].replace("T", " ").replace("Z", "+00:00")
            else:
                event_time = datetime.fromtimestamp(time.time())
                temp_dict["datetime"] = datetime.fromtimestamp(time.time())
            temp_dict["date"] = datetime.strftime(event_time, "%a, %d %b %Y")
            temp_dict["time"] = datetime.strftime(event_time, "%I:%M %p")
            temp_dict["ticketmaster_id"] = event["id"]
            events.append(temp_dict)

        return events, len(response["_embedded"]['events'])
    else:
        return [], 0


def image_selector(images):
    """
    Selects the highest resolution 16x9 image
    Args:
        images (array): An array of ticketmaster image objects
    """
    best_image = images[0]
    for image in images:
        # The 16x9 aspect ratio fits really well, unless you resize the page ):
        if image["ratio"] == "16_9":
            # On second thought, this is probably a waste of bandwidth. Oh well.
            if image["width"] > best_image["width"]:
                best_image = image
    return best_image

