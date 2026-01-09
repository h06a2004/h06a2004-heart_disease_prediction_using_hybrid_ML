import os
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages

from user.models import UserRegisteredTable

# Create your views here.
def userHome(request):
    return render(request,'users/userHome.html')
def userRegister(request):
    if request.method == 'POST':
        # Extract data from the request
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        loginid = request.POST.get('loginid')
        mobile = request.POST.get('mobile')
        locality = request.POST.get('locality')  # Locality
        state = request.POST.get('state')  # State

        user = UserRegisteredTable(
            name=name,
            email=email,
            password=password,  # Password will be hashed in the model's save method
            loginid=loginid,
            mobile=mobile,
            locality=locality,
            state=state,
        )
        print(user.name)
        try:
            if user.full_clean:
                user.save()

                messages.success(request, 'Registration successful!.')
                return render(request,'register.html')  # Redirect to the login page or another page as needed
            else:
                messages.error(request,'Entered data is in valid')
                return render(request,'register.html')
        except:
            messages.error(request,'Entered data not valid ')
            return render(request,'register.html')


    return render(request, 'register.html')

def userLoginCheck(request):
    if request.method=="POST":
        loginid=request.POST['loginid']
        password=request.POST['password']
        print(loginid,password)
        try:
            user=UserRegisteredTable.objects.get(loginid=loginid,password=password)
            status=user.status
            print(status)
            if status=='activated':
                return render(request,'users/userHome.html')
            else:
                messages.error(request,'Status Not Activated')
                return render(request,'userLogin.html')
        except:
            messages.error(request,'Invalid details')
            return render(request,'userLogin.html')
    else:
        return render(request,'userLogin.html')
    
import numpy as np
import joblib
from django.shortcuts import render
from django.http import HttpResponse

# Load trained model and scaler
model = joblib.load("best_model.pkl")  # Load trained model
scaler = joblib.load("scaler.pkl")  # Load trained scaler

def predict_heart_disease(request):
    if request.method == "POST":
        try:
            # Extract user input from the form
            age = float(request.POST.get("age"))
            sex = int(request.POST.get("sex"))
            chest_pain_type = int(request.POST.get("chest_pain_type"))
            resting_bp_s = float(request.POST.get("resting_bp_s"))
            cholesterol = float(request.POST.get("cholesterol"))
            fasting_blood_sugar = int(request.POST.get("fasting_blood_sugar"))
            resting_ecg = int(request.POST.get("resting_ecg"))
            max_heart_rate = float(request.POST.get("max_heart_rate"))
            exercise_angina = int(request.POST.get("exercise_angina"))
            oldpeak = float(request.POST.get("oldpeak"))
            st_slope = int(request.POST.get("st_slope"))

            # Convert user input into an array
            user_input = np.array([
                age, sex, chest_pain_type, resting_bp_s, cholesterol,
                fasting_blood_sugar, resting_ecg, max_heart_rate, exercise_angina,
                oldpeak, st_slope
            ]).reshape(1, -1)

            # Scale the input using the trained scaler
            user_input_scaled = scaler.transform(user_input)

            # Make prediction
            prediction = model.predict(user_input_scaled)[0]

            # Convert numeric prediction to a readable format
            prediction_result = "High Risk" if prediction == 1 else "Low Risk"

            return render(request, "users/predictionForm.html", {"prediction": prediction_result})

        except Exception as e:
            return HttpResponse(f"Error processing request: {e}")

    return render(request, "users/predictionForm.html")



from user.utility.requirement  import main
def classificationView(request):
    svm_acc, dt_acc, ann_acc,hmm_acc,best_model_name=main()
    return render(request,'users/classificationView.html',context={'svm_acc':svm_acc,'dt_ac':dt_acc,'ann_ac':ann_acc,'hmm_ac':hmm_acc,'best_model':best_model_name})


import pandas as pd
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse

def dataset(request):
    try:
        # Load dataset
        df = pd.read_csv('media/heart-disease-dataset.csv')

        # Pagination setup (show 10 rows per page)
        paginator = Paginator(df.to_dict(orient="records"), 10)  # Convert DataFrame to list of dicts
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        return render(request, 'users/dataset.html', {"page_obj": page_obj})

    except FileNotFoundError:
        return HttpResponse("Dataset file not found. Please check the file path.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
