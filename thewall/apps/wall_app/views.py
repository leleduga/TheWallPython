from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from . models import *
import bcrypt

def index(request):
    if "errors" in request.session:
        errors=request.session["errors"]
        firstname=request.session["firstname"]
        lastname=request.session["lastname"]
        email=request.session["email"]
        del request.session["errors"]
    else:
        errors=[]    
        firstname=""
        lastname=""
        email=""

    context={
        "errors":errors,
        "firstname":firstname,
        "lastname": lastname,
        "email": email,
    }
    return render(request, 'wall_app/index.html', context)

def create(request):
    data_is_valid, errors = User.objects.basic_validator(request.POST)
    print ('data is valid',data_is_valid)
    print (errors)
    if  data_is_valid:    
        user_login= User.objects.create(
            firstname=request.POST["firstname"],
            lastname=request.POST["lastname"],
            email=request.POST["email"],
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()),

        )
        request.session['firstname']=request.POST["firstname"]
        request.session['lastname']=request.POST['lastname']
        request.session['email']=request.POST['email']

        return redirect('/wall')
    else:
        request.session["errors"]=errors
        request.session['firstname']=request.POST["firstname"]
        request.session['lastname']=request.POST['lastname']
        request.session['email']=request.POST['email']
        return redirect('/') 

def validate_login(request):
    user = User.objects.get(email=request.POST['email'])
    print(user.email)
    print(user.password)
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['email'] = request.POST['email']
        request.session['firstname']=user.firstname
        print("password match")
        return redirect('/wall')
    else:
        request.session["errors"]=errors
        print("failed password") 
        return redirect('/')    

def wall(request):
    messages= Message.objects.all().order_by('-created_at')
    comments = Comment.objects.all().order_by('-created_at')
    user= User.objects.get(email=request.session['email'])

    context = {
      "messages" : messages,
      "user":user,
    }
    return render(request, 'wall_app/wall.html', context)

def msuccess(request):
    user= User.objects.get(email=request.session['email'])
    message=Message.objects.create(
        message=request.POST['message'],
        user=user,
    )
    return redirect('/wall')

def csuccess(request, id):
    message=Message.objects.get(id=id)
    user= User.objects.get(email=request.session['email'])
    comment=Comment.objects.create(
        comment=request.POST['comment'],
        user=user,
        cmessage= message,
    )
    return redirect('/wall')

def logout(request):
    del request.session['email']
    return render(request, 'wall_app/logout.html')
