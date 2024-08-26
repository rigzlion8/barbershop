from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment, Service
from .forms import AppointmentForm

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('appointment_confirmation')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book.html', {'form': form})

@login_required
def appointment_confirmation(request):
    return render(request, 'appointments/confirmation.html')
