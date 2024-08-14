from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=user.pk)
    else:
        form = UserCreationForm(instance=user)
    return render(request, 'accounts/edit_user.html', {'form': form})