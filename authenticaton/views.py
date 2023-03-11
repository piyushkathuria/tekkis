from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required



# Create your views here.
class SignUpView(CreateView):
    template_name = "authentication/signup.html"
    model = User
    fields = ['username', 'email', 'password']
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        # Hash the user's password before saving to the database
        form.instance.set_password(form.cleaned_data['password'])
        return super().form_valid(form)


class LoginView(View):
    template_name = "authentication/login.html"
    success_url =reverse_lazy('todo/create')
    
    def get(self, request):
        # Redirect authenticated users to the user list view
        if request.user.is_authenticated:
            return redirect('userslist')
        
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validate user input
        if not username or not password:
            return render(request, self.template_name, {'error': 'Invalid username or password.'})
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_active:
            # Login user and redirect to the todo list view
            login(request, user)
            return redirect('success_url')
        
        return render(request, self.template_name, {'error': 'Invalid username or password.'})


class UserList(ListView):
    login_required = True
    template_name="authentication/profile_list.html"
    model = User



class UserDetailView(DetailView):
    template_name="authentication/profile_detail.html"
    # specify the model to use
    model = User



class UserUpdate(UpdateView):
    template_name="authentication/update_profile.html"
    model = User
    fields=['username','email','password']
    success_url="/userslist"
    

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')