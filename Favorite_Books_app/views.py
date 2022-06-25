from django.contrib import messages
from django.shortcuts import render ,redirect
import bcrypt
from .models import *

def index(request):
    return render(request,"index.html")



def register(request):
    if request.method =='POST':
        errors=users.objects.validator(request.POST)
        if len(errors) > 0:
            for key , value in errors.items():
                messages.error(request,value)
            
            return redirect('/')
        else:
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            email=request.POST['email']
            password=request.POST['password']
            pwhash=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            new_user=users.objects.create(first_name=first_name,last_name=last_name,email=email,password=pwhash)
            new_user.save()
            request.session['loggedIn'] = new_user.id
            return redirect('/books')


def login(request):
    if request.method=='POST':
        users_all = users.objects.filter(email=request.POST['email'])
        if len(users_all)==1:
            if not bcrypt.checkpw(request.POST['password'].encode(),users_all[0].password.encode()):
                messages.error(request, "Email or Password is incorrect!")
                return redirect('/')
            else:
                request.session['loggedIn'] = users_all[0].id
                return redirect('/books')
        else:
            messages.error(request, "Email does not exist!")
            return redirect('/')



def books(request):
    if not 'loggedIn'in request.session:
        return redirect('/')
    else:
        context={
        'users':users.objects.get(id=request.session['loggedIn']),
        'books' : Books.objects.all(),
    }
    return render (request,'books.html',context)
    
def book(request,id):
    Tbook=Books.objects.get(id=id)
    Tuser=users.objects.all()
    Tlike=Books.objects.get(id=id).users_who_like.filter(id=request.session['loggedIn'])
    context = {
        'Tuser' : Tuser,
        'Tbook' :Tbook,
        'Tlike': Tlike
    }
    return render (request,'book.html',context)

def add_book(request):
    if request.method == 'POST':
        errors=Books.objects.Bvalidate(request.POST)
        if len((errors)) > 0:
            for key , value in errors.items():
                messages.error(request,value)
            return redirect('/books')
        else:
            title=request.POST['title']
            description=request.POST['description']
            uploaded_by=users.objects.get(id=request.session['loggedIn'])
            newBook=Books.objects.create(title=title,description=description,uploaded_by=uploaded_by)
            newBook.users_who_like.add(uploaded_by)
            newBook.save()
            messages.success(request, "Book is successfully added!")
            return redirect('/books')

def edit_book(request,id):
    if request.method == 'POST':
        errors=Books.objects.Bvalidate(request.POST)
        if len((errors)) > 0:
            for key , value in errors.items():
                messages.error(request,value)
            return redirect(f'/books/{id}')
        else:
            book=Books.objects.get(id=id)
            book.title=request.POST['title']
            book.description=request.POST['description']
            book.save()
            messages.success(request, "Book is successfully updated!")
            return redirect('/books')
    else:
        return redirect(f'/books/{id}')

def delete_book(request,id):
    book=Books.objects.get(id=id)
    if request.session['loggedIn'] == book.uploaded_by.id:
        book.delete()
    messages.success(request, "Book is successfully deleted!")
    return redirect('/books')


def favoriteBook(request,id):
    Tuser= users.objects.get(id= request.session['loggedIn'])
    liked_book=Books.objects.get(id=id)
    liked_book.users_who_like.add(Tuser)
    messages.success(request, "Book is successfully added to Favorites!")
    return redirect(f'/books/{id}')

def unfavoriteBook(request,id):
    Tuser=users.objects.get(id= request.session['loggedIn'])
    liked_book=Books.objects.get(id=id)
    liked_book.users_who_like.remove(Tuser)
    messages.success(request, "Book is successfully removed from Favorites!")
    return redirect(f'/books/{id}')

def logout(request):
    request.session.clear()
    return redirect('/')
