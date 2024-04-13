from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .python_robotcontroller.video_reciever import start_video_server
from .python_robotcontroller.game import start_robot
from .python_robotcontroller.server.client import client
import json
import pygame

# Global variables
port = 8001
server = "0.0.0.0"

def playsound(sound):
    pygame.mixer.init()
    pygame.mixer.music.load(f'{sound}.wav')
    pygame.mixer.music.play()

def index(request):
    return render(request, 'home.html')

def home(request):
    return render(request, 'home.html')

def information(request):
    return render(request, 'information.html')

def settings(request):
    return render(request, 'settings.html')

def start(request):
    print(f"Starting robot at {server}:{port}...")
    if server == "0.0.0.0":
        tkintermessage("Please enter a server address in the settings page")
    else:
        start_robot(server, port)
    return HttpResponse("")

def forward(request):
    client("forward", server, port)
    return HttpResponse("")
def backward(request):  
    client("backward", server, port)
    return HttpResponse("")
def left(request):
    client("left", server, port)
    return HttpResponse("")
def right(request):
    client("right", server, port)
    return HttpResponse("")

def camera(request):
    if server == "0.0.0.0":
        tkintermessage("Please enter a server address in the settings page")
    else:
        print("Opening camera..")
        start_video_server()
    return HttpResponse("")

def sound(request):
    if server == "0.0.0.0":
        tkintermessage("Please enter a server address in the settings page")
    else:
        print("Playing sound..")
        client("alarm_sound", server, port)
    return HttpResponse("")

def shutdown(request):
    if server == "0.0.0.0":
        tkintermessage("Please enter a server address in the settings page")
    else:
        print("Shutting down robot..")
        client("over_sound", server, port)
    return HttpResponse("")

def savesettings(request):
    global port
    global server

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        server = data.get('robotIP')
        port = int(data.get('port'))
        print("Saving settings... Robot IP:", server, "Port:", port)
        try:
            client("test", server, port)
        except Exception as e:
            print(f"Cause of error: {e}")

    return HttpResponse("")

def Contact(request):
    return redirect("/Contact")

def sendmessage(request):
    if server == "0.0.0.0":
        tkintermessage("Please enter a server address in the settings page")
    else:
        start_robot(server, port)
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            message = data.get('message')
            print("Sending message: " + message)
            client("word"+message, server, port)
    return HttpResponse("")
