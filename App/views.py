from django.shortcuts import render, redirect
import requests
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.

def index(request):
    loading = True
    context={"loading":loading}

    if not 'loaded' in request.GET:
        return render(request,"index.html", context)
    

    url = 'https://dummyjson.com/recipes'
    data = requests.get(url).json()
    loading = False
    context = {
        "loading":False,
        "data" : data["recipes"],
    }
    return render(request,"index.html", context)

def recipeDetails(request,id):
    url= f'https://dummyjson.com/recipes/{id}'
    data = requests.get(url).json()
    ingredients = data["ingredients"]
    context = {
        "data":data,
        "ingredients" : ingredients,
        "instructions" : data["instructions"]
    }
    return render(request,"recipedetails.html", context)

def searchedRecipe(request):
    if request.method == "POST":
        value = request.POST.get("value")
        url= f'https://dummyjson.com/recipes/search?q={value}'
        data = requests.get(url).json()
    context={
        "data_searched": data["recipes"]
    }
    return render(request, "index.html",context)

def mealType(request, meal):
    url= f"https://dummyjson.com/recipes/meal-type/{meal}"
    data = requests.get(url).json()
    context={
        "data": data["recipes"]
    }
    return render(request,"index.html",context)

def login(request):
    return render(request,"login.html")

def register(request):
    return render(request,"register.html")

def registerUser(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        password  = request.POST.get("pass")

        hased_pass = make_password(password)
        try:
            if User.objects.filter(email=email).exists():
                messages.success(request,"Account Already Exists!")
                return redirect(login)
            
            else:

                saveUser = User(name=name,phone=phone,email=email,gender=gender,password=hased_pass)
                saveUser.save()
                messages.success(request,"Account Created Successfully!")
                return redirect(login)
        except:
            pass
    return render(request,"register.html")

def loginuser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pass")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,"User Does not Exists! ")
            return redirect(login)

        if check_password(password, user.password):
            request.session["login_id"] = user.id
            request.session["login_name"] = user.name
            request.session["login_email"] = user.email
            request.session.set_expiry(7200)
            messages.success(request,"Login Successful")
            return redirect(index)
        else:
            messages.error(request,"Invalid Password")
            return redirect(login)
    return render(request,"login.html")

def logout(request):
    try:
        del request.session["login_id"]
        del request.session["login_name"]
        del request.session["login_email"]
        return redirect(login)
    except:
        pass
    return render(request,"login.html")

def favourite(request):
    uid = request.session.get("login_id")
    if not uid:
        messages.error(request,"PLz Login first!")
        return redirect(login)
    
    favs = Favourite.objects.filter(user=uid)
    recipes=[]
    for fav in favs:
        url= f'https://dummyjson.com/recipes/{fav.recipe}'
        data = requests.get(url).json()
        data["fav_id"] = fav.id
        recipes.append(data)

    context = {
        "data": recipes
    }
    return render(request,"favourite.html",context)

def addToFavourite(request,id):
    uid = request.session.get("login_id")

    if not uid:
        messages.error(request,"You need to Login First!")
        return redirect(login)
    
    if Favourite.objects.filter(user=uid,recipe=id).exists():
        messages.error(request,"Recipe Already Added in favourites!")
        return redirect(index)
    try:
        saveRecipe = Favourite(user=User(id=uid),recipe=id)
        saveRecipe.save()
        messages.success(request,"Recipe has been Saved to faviourite.")
        return redirect(index)
    except:
        pass
    return render(request,"favourite.html")

def deletefav(request,id):
    uid = request.session["login_id"]
    try:
        fav = Favourite.objects.get(id=id, user=uid)
        fav.delete()
        messages.success(request,"Recipe Removed From Favourites")
        return redirect(favourite)
    except:
        pass
    return render(request,"favourite.html")