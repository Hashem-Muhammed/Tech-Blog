from django.shortcuts import render,get_object_or_404,HttpResponseRedirect , redirect
from django.views import View
from blog.models import Author , Post , Tag , Comment
from .forms import RegisterForm, AddPostForm, LoginForm, SettingsForm, CommentForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import UserCreationForm  
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def index(request):
    ALL_POSTS = Post.objects.all()
    latest_posts = ALL_POSTS.order_by("-date")[:2]
    message = ""
    if 'id' in request.session:
        user_id = request.session.get('id')
        author = Author.objects.get(id = user_id)
        message= f"Welcome {author.first_name}"
        print(message)
    
    return render(request, "blog/index.html", {"latest_posts":latest_posts , "message": message})



@login_required(login_url='login')

def all_posts(request):
    ALL_POSTS = Post.objects.all()
    return render(request, "blog/all-posts.html", {"posts" : ALL_POSTS  })   



@login_required(login_url='login')

def post_datails(request, slug):
    identified_post = get_object_or_404(Post , slug=slug)
    tags=identified_post.tag.all()
    if request.method == 'POST': 
        form = CommentForm(request.POST)
        user= request.user
        print("here")
        if form.is_valid():
            text = form.cleaned_data['content']
            comment = Comment (content= text , author = user , post = identified_post )
            comment.save()
            post_id = identified_post.slug
            path = '/posts/' + post_id
            return redirect (path)
    else:
        comments = identified_post.comment_post.all()
        form = CommentForm()
        return render(request, "blog/details.html", {
            "post" : identified_post ,
             "tags" : tags ,
              "form":form,
              "comments":comments
            })   



def AuthorRegister(request):
    if request.method == 'POST':
        form = RegisterForm (request.POST)
        #print(form.cleaned_data.get('email'))
        if form.is_valid():
            print("valid")
            form.save()    
            return redirect("login")
        else:
           return render(request , "blog/register.html", {"form":form} )

    else:
        form = RegisterForm()
        return render(request , "blog/register.html", {"form":form} )



@login_required(login_url='login')

def addPost(request):
    if request.method=='POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)

            form.save()
            return redirect('Home')
        else:
            return render(request , "blog/add-new-post.html", {"form":form} )
    else:
        form =AddPostForm()
        return render(request , "blog/register.html", {"form":form} )
    


def log_out(request):
    logout(request)
    return redirect('login')    



class profileSettings(View):
    def post(self, request):
        user = request.user
        form = SettingsForm(request.POST , request.FILES , instance=user)
        if form.is_valid():
            form.save()
            return redirect('profilesettings')
        else:
            return render(request, 'blog/profilesettings.html' , {"form" : form})    


    def get(self,request):
        user = request.user
        form = SettingsForm(instance=user)
        print(user)
        return render(request, 'blog/profilesettings.html' , {"form" : form})               

    
# def login(email , password):
#     if Author.objects.filter(email = email, password = password).exists():
#         return True
#     else:
#         return False
# class LogIn(View):
    
#     def post(self,request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             print (form.cleaned_data['email'])
#             loggedin = login(form.cleaned_data['email'],form.cleaned_data['password'])
#             if loggedin:
#                 author = Author.objects.get(email = form.cleaned_data['email'])
#                 request.session["id"] = author.pk
#                 return HttpResponseRedirect("/")
#             else:
#                 message = "Wrong username or password!"
#                 print(loggedin)
#                 return render(request , "blog/login.html" , {"form" : form , "message":message , "loggedin":loggedin})    
#     def get(self,request):
#             form = LoginForm()
#             return render(request , "blog/login.html" , {"form" : form })

class LogIn(View):
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            print (form.cleaned_data['email'])
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username= username , password = password )
            print(username , password , user)
            if user is not None:
                login(request , user)
                print('nothing wrong')
                return HttpResponseRedirect("/")
            else:
                message = "Wrong username or password!"
                return render(request , "blog/login.html" , {"form" : form , "message":message })    
    def get(self,request):
            form = LoginForm()
            return render(request , "blog/login.html" , {"form" : form })


class AddComment(View):
    def post(self,request,slug):
        form = CommentForm(request.POST)
        user= request.user
        identified_post = get_object_or_404(Post , slug=slug)
        if form.is_valid():
            text = CommentForm.cleaned_data['content']
            comment = Comment (content= text , comment_author = user , comment_post = identified_post )
            comment.save()
            post_id = identified_post.slug
            path = 'blog/details.html' + post_id
            return redirect ('Home')

    def get(self,request,slug):
        form = CommentForm()
        identified_post = get_object_or_404(Post , slug=slug)
        post_id = identified_post.slug
        path = 'blog/details.html' + post_id
        return render(request, path,  {"form":form , "post" : identified_post ,"tages": identified_post.tag.all()} )        


