from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import View
from django.contrib.auth.models import User
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
        # Check if username is already taken
        if User.objects.filter(username=form.cleaned_data['username']).exists():
            form.add_error('username', 'Username is already taken.')
            return super().form_invalid(form)

        # Check if email is already taken
        if User.objects.filter(email=form.cleaned_data['email']).exists():
            form.add_error('email', 'Email is already taken.')
            return super().form_invalid(form)

        # Check password length
        password = form.cleaned_data['password']
        if len(password) < 8:
            form.add_error('password', 'Password must be at least 8 characters long.')
            return super().form_invalid(form)

        # Hash the user's password before saving to the database
        form.instance.set_password(password)
        return super().form_valid(form)


class LoginView(View):
    template_name = "authentication/login.html"
    success_url = '/todo/create/'
    
    
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
            return redirect(self.success_url)
        
        return render(request, self.template_name, {'error': 'Invalid username or password.'})

    def get(self, request):
        # Redirect authenticated users to the user list view
        if request.user.is_authenticated:
            return render(request,'authentication/login.html')
        
        return render(request, self.template_name)


# class UserList(ListView):
#     login_required = True
#     template_name="authentication/profile_list.html"
#     model = User



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