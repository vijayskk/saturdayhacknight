from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import warnings
import joblib
import platform
import os

def warn(*args, **kwargs):
    pass

warnings.warn = warn

model = joblib.load("fakepredict/modell.joblib")

def askYN(qn):
    inp = input(qn)
    if 'y' in inp:
        return 1
    else:
        return 0

def askInt(qn):
    inp = input(qn)
    return int(inp)

def askFloat(qn):
    inp = input(qn)
    return float(inp)

def calcDigits(string):
    digit = 0
    for ch in string:
        if ch.isdigit():
            digit = digit + 1
        else:
            pass
    return digit

def clearTerminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def printUnderlined(text):
    print(f"\033[4m{text}\033[0m")

def printNewline(n):
    for i in range(n):
        print("\n")

@csrf_exempt
def predict_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        pp = int(request.POST.get('profile_picture'))
        numbylenu = calcDigits(username) / len(username)
        fullnamewords = len(fullname.split(' '))
        numbylenf = calcDigits(fullname) / len(fullname)
        nameeqfull = username == fullname
        dlength = len(request.POST.get('description').replace(" ", ""))
        haveURL = int(request.POST.get('external_link'))
        isPrivate = int(request.POST.get('private_account'))
        posts = int(request.POST.get('posts'))
        followers = int(request.POST.get('followers'))
        follows = int(request.POST.get('following'))

        pred = model.predict([[pp, numbylenu, fullnamewords, numbylenf, nameeqfull, dlength, haveURL, isPrivate, posts, followers, follows]])

        if pred[0] == 1:
            result = "The account is fake"
        else:
            result = "The account is NOT fake"

        return HttpResponse(result)

    return HttpResponse("Bad Request")

def home(request):
    print("Here")
    return render(request , "home.html")