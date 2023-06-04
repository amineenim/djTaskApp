
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login 
from .models import Task
# Create your views here.


# class based view to login users 
class CustomLogin(LoginView) :
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self) :
        return reverse_lazy('tasks')

# class based view to register new users 
class CustomRegister(FormView) :
    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')
    redirect_authenticated_user = True 

    # after the form is submitted and valid 
    def form_valid(self, form) :
        user = form.save()
        if user is not None :
            login(self.request, user)
        return super(CustomRegister, self).form_valid(form)
    
    def get(self, *args, **kwargs) :
        if self.request.user.is_authenticated :
            return redirect('tasks')
        return super(CustomRegister, self).get(*args, **kwargs)
    
# this is a class based View, it displays all tasks 
class TaskList(LoginRequiredMixin, ListView) :
    model = Task 
    # define a custom name for the list of items we get for the view
    context_object_name = 'tasks'
    # it by default looks for a view named task_list.html

    #override this function so only a user can view his tasks
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False)
        # add the search functionnality 
        search_input = self.request.GET.get('search-area') or ''
        if search_input :
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context 
    

# this is a class based view, it's purpose is to display a unique task detail 
class TaskDetail(LoginRequiredMixin, DetailView) :
    model = Task 
    # it looks by default for a view named task_detail.html
    # customize the name of the object 
    context_object_name = 'task'
    # customize the name of the template 
    template_name = 'base/task.html'


# class based view in charge of creating a new Task 
class TaskCreate(LoginRequiredMixin, CreateView) :
    # it looks for a view with the name task_form.html 
    model = Task 
    # list the fields wanted on the create form
    fields = ['title', 'description', 'complete']
    # define the url to redirect to after a success submit of the create form
    success_url = reverse_lazy('tasks')

    # override this function so the user is automatically set 
    def form_valid(self, form) :
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

# class based view handling updating a Task object 
class TaskUpdate(LoginRequiredMixin, UpdateView) :
    # by default it looks for a view with the name task_form.html 
    model = Task 
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

# class based view in charge of deleting a task object 
class TaskDelete(LoginRequiredMixin ,DeleteView) :
    # by default it expects a view named task_confirm_delete.html
    # which send a delete request via post method so it contains a form
    model = Task 
    success_url = reverse_lazy('tasks')
    # the name passed to the delete confirmation view
    context_object_name = 'task'
    template_name= 'base/task_delete.html'