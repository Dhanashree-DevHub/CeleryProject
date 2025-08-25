from django.shortcuts import render
from .tasks import dummy_and_slow 
import time
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse  # Add this line
from .models import Report
from mainapp.forms import FeedbackForm
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
def index(request):
    return render(request, 'mainapp/index.html')

def dummy_and_slow_view(request):
    start_time = time.time()
    dummy_and_slow.delay()
    end_time=time.time()
    execution_time = end_time - start_time
    context = {"task_name": "Dummy and slow", "execution_time": round(execution_time, 2)}
    return render(request, 'mainapp/generic.html', context=context)

# Create your views here.
class ReportCreateView(CreateView):
    model = Report
    fields = ['complexity']
    template_name = 'mainapp/report_form.html'
    
    def get_success_url(self):
        return reverse('report_detail', kwargs={'pk': self.object.pk})
class ReportDetailView(DetailView):
    model = Report
    context_object_name = 'report'
    template_name = 'mainapp/report_detail.html'
    
class ReportListView(ListView):
    model = Report
    template_name = "mainapp/report_list.html"
    context_object_name = "reports"
    ordering = ["-dt_created"]
    paginate_by = 10
    
    
class FeedbackFormView(FormView):
    template_name = "mainapp/feedback_form.html"
    form_class = FeedbackForm
    success_url = "/thanks/"

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
    
class ThanksView(TemplateView):
    template_name = "mainapp/thanks.html"