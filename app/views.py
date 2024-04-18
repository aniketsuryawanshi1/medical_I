from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .auth import authentication
from .forms import InsuranceForm
import numpy as np
import pickle
# Create your views here.

model = pickle.load(open(r'D:\Django\clg_class\New folder\kk\kajal\medical_I\app\MedicalInsuranceCost.pkl', 'rb'))
                    


def home(request):
    return render(request,'base.html')

def registration(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        
        # Verify password and register user
        verify = authentication(name, password, repassword)
        if verify == "success":
            # Create a new user
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()
            
            # Display success message
            messages.success(request, "Your Account has been Created.")
            print("User has been created")
            # Render the registration form template with the success message
            return render(request, "log_in.html")
        else:
            # Display error message
            messages.error(request, verify)
    
    # Render the registration form template
    return render(request, "log_in.html")

def log_in(request):
    if request.method == "POST":
        username = request.POST['username']  # Assuming email is used as username
        password = request.POST['password']

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            print("User logged in successfully")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    return render(request, "log_in.html")
@login_required(login_url="log_in")

def dashboard(request):
    return render(request,'dashboard.html')



@login_required(login_url="log_in")

def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")


def view(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')


#******************************************Accept User Form******************************************************
def predict(request):
    form  = InsuranceForm()
    return render(request, 'predict.html', {'form' : form})
#******************************************Prediction Logic******************************************************

def prediction(request):
    if request.method == 'POST':
        form = InsuranceForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']
            bmi = form.cleaned_data['bmi']
            smoker = form.cleaned_data['smoker']
            region = form.cleaned_data['region']
            children = form.cleaned_data['children']

            sex_male = 1 if sex == 'male' else 0 
            smoker_yes = 1 if smoker == 'yes' else 0

            region_dict = {'northwest': [1, 0, 0, 0], 'southeast': [0, 1, 0, 0], 'southwest': [0, 0, 1, 0], 'northeast': [0, 0, 0, 1]}
            region_values = region_dict.get(region, [0, 0, 0, 0])

            values = np.array([[age, sex_male, smoker_yes, bmi, children] + region_values])
            prediction = model.predict(values)
            prediction = round(prediction[0], 2)

            return render(request, 'result.html', {'name': name, 'prediction_text': 'Estimated medical insurance cost is {}'.format(prediction)})
    else:
        form = InsuranceForm()
    return render(request, 'index.html', {'form': form})