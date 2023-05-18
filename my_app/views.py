from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from my_app.models import Room
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from my_app.forms import RegisterUserForm

# Create your views here.
@login_required(login_url='login/')
def index(request):
    if request.method == 'POST':
        roomId = request.POST.get("room-id", None) #get from the "form" in the index.html
        playerId = request.user.id
        
        if(roomId):
            try: 
                room = Room.objects.get(roomNumber=roomId)
                return redirect(f"/game/{room.roomNumber}/{playerId}/") #send to this endpoint
            except Room.DoesNotExist:
                room = Room(roomNumber=roomId)
                room.save() #create new model in the "models.py"
                return redirect(f"/game/{room.roomNumber}/{playerId}/")
        else:
            messages.error(request, "You need to choose a room!")
            return redirect("/") #send to this endpoint 
    
    return render(request, "index.html")

@login_required(login_url='login/')
def game(request, roomNumber=None, playerId=None):
    try:
        room = Room.objects.get(roomNumber=roomNumber)
        player = request.user.username
        playerId = request.user.id
        return render(request, "game.html", {"room": room, "playerId": playerId, "name": player  }) #this will be send to the browser to ew get in the html page those attributes
    except Room.DoesNotExist:
        messages.error(request, "Room does not exist, fool!")
        return redirect("login/")

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        print(form.errors)  # add this line to print form errors
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterUserForm()
    
    context = {
        'form': form
    }
    return render(request, 'register.html', context)
    

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        messages.info(request, 'Username OR password is incorrect')
        return render(request, 'login.html', )
        
    return render(request, "login.html")


def logoutPage(request):
    logout(request)
    return redirect('login')