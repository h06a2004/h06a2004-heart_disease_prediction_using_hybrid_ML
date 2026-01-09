from django.shortcuts import render
from django.contrib import messages

from user.models import UserRegisteredTable

# Create your views here.

def adminLoginCheck(request):
    if request.method=="POST":
        login_id=request.POST['loginid']
        password=request.POST['password']

        if login_id=='admin' and password=='admin':
            return render(request,'admin/adminHome.html')
        else:
            messages.error(request,'Invalid details')
            return render(request,'adminLogin.html')
    else:
        return render(request,'adminLogin.html')
        
def adminHome(request):
    return render(request,'admin/adminHome.html')

def userDetails(request):
    user=UserRegisteredTable.objects.all()
    return render(request,'admin/userDetails.html',{'user':user})

def activateUser(request):
    loginid=request.GET['loginid']
    user=UserRegisteredTable.objects.get(loginid=loginid)
    user.status='activated'
    user.save()
    userr=UserRegisteredTable.objects.all()
    return render(request,'admin/userDetails.html',{'user':userr})

def deactivateUser(request):
    loginid=request.GET['loginid']
    user=UserRegisteredTable.objects.get(loginid=loginid)
    user.status='Waiting'
    user.save()
    userr=UserRegisteredTable.objects.all()
    return render(request,'admin/userDetails.html',{'user':userr})


from user.utility.requirement  import main
def adminclassificationView(request):
    svm_acc, dt_acc, ann_acc,hmm_acc,best_model_name=main()
    return render(request,'admin/adminClassificationView.html',context={'svm_acc':svm_acc,'dt_ac':dt_acc,'ann_ac':ann_acc,'hmm_ac':hmm_acc,'best_model':best_model_name})


            

