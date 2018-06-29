from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,TemplateView,FormView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from accounts.forms import UserCreationForm,UserChangeForm,UserEditForm,UserLoginForm,StudentFetchForm,EventAddForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.views import password_reset
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from .models import MyUser
from events.models import EventModel

@login_required
def register(request):
    if request.method == 'GET':
        form=UserCreationForm()
        return render(request,'registration.html',{'form':form,'student_list' :MyUser.objects.exclude(pk=1)})

    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('registrationsuccess'))
        else:
            return render(request,"registration.html",{'form':form})

    else:
        form =UserCreationForm()
    return render(request, 'login.html', {
        'form': form
    })

@login_required
def add_event(request):
    if request.method == 'GET':
        form=EventAddForm()
        return render(request,'event_add.html',{'form':form})

    if request.method == 'POST':
        form = EventAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('teacher_home'))
        else:
            return render(request,"event_add.html",{'form':form})

    else:
        form =EventAddForm()
    return render(request, 'event_add.html', {
        'form': form
    })

class LoginView(View):
    form_class = UserLoginForm
    template_name="login.html"

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self, request):
        password = request.POST['password']
        username = request.POST['username']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                if user.is_staff:
                    login(request,user)
                    query=MyUser.objects.get(id=user.id)
                    return HttpResponseRedirect(reverse('teacher_home'))
                else:
                    login(request,user)
                    query=MyUser.objects.get(id=user.id)
                    return HttpResponseRedirect(reverse('student_home'))

            else:
                return HttpResponse("Inactive user.")
        else:
            # return redirect("IITApp:login")
            return render(request, 'login.html',{
            'login_message' : 'Enter the username and password correctly',})

        return render(request, "login.html")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")
    
def StudentListView(request):
    class_list=[]
    obj_list=[]
    data=[]
    class_names=MyUser.objects.values('class_name').order_by('class_name')
    for klass in class_names:
        class_list.append(klass['class_name'])
    class_list=sorted(set(class_list))
    for clas in class_list:
        li=MyUser.objects.filter(class_name=clas).exclude(pk=1).order_by('username')
        obj_list.append(clas)
        for obj in li:
            obj_list.append(obj)
    for index in range(len(obj_list)):
        obj = obj_list[index]
        temp={}
        lis = []
        if isinstance(obj,int):
            i = index
            try:
                while(not isinstance(obj_list[i+1],int)): 
                    lis.append(obj_list[i+1])
                    i+=1
            except:
                pass
            temp[obj] = lis
            data.append(temp)
    obj_list=data
    context={'obj_list':obj_list}
    return render(request,'studentlist.html',context)
            
        
class StudentFetchView(LoginRequiredMixin,FormView):
    form_class= StudentFetchForm
    template_name='user_fetch_form.html'

def student_fetch(request):
    try:
        class_name=request.POST['class_name']
    except:
        print('cant fetch the vvalue of class_num')
    result_set=[]
    selected_users=[]
    answer=int(class_name)
    student_none="No Student Yet!"
    pk_NA= "NA"
    selected_users=MyUser.objects.filter(class_name=answer).exclude(pk=1)
    if selected_users:
        for user in selected_users:
                result_set.append({'name':user.username,'pk':user.id})
    else:
        result_set.append({'name':student_none,'pk':pk_NA})

    return JsonResponse({'result_set' : result_set})
 
 

class StudentDetailView(LoginRequiredMixin,DetailView):
    queryset = MyUser.objects.exclude(pk=1)
    model=MyUser
    template_name='studentdetail.html'
    context_object_name='student'
  

@login_required
def teacherHomeView(request):
    events_list=[]
    eventsList=EventModel.objects.all().order_by('occur_date')
    if eventsList:
        for event in eventsList:
            events_list.append({'occur_date':event.occur_date,'content':event.content,'id':event.id})
    context={'events_list':events_list}
    return render(request,'home_teacher.html',context)


class StudentHomeView(LoginRequiredMixin,TemplateView):
    template_name="home_student.html"



class UpdateUserView(LoginRequiredMixin,UpdateView):
    queryset=MyUser.objects.exclude(pk=1)
    template_name='update.html'
    form_class=UserEditForm
    success_url= '/editconfirm/'

        
    
class DeleteUserView(LoginRequiredMixin,DeleteView):
    model=MyUser
    template_name='delete.html'
    success_url='/deleteconfirm/'
    
  
class RegistrationSuccessView(LoginRequiredMixin,TemplateView):
    template_name="registrationsuccess.html"

class EditConfirmView(LoginRequiredMixin,TemplateView):
    template_name="editconfirm.html"
    
class DeleteConfirmView(LoginRequiredMixin,TemplateView):
    template_name="deleteconfirm.html"

def DeleteEventView(request,**kwargs):
    id= kwargs['id']
    EventModel.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('teacher_home'))