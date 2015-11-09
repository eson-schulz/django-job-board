from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CompanyForm, UserForm, CompanyUpdateForm


def register(request):

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        company_form = CompanyForm(data=request.POST)

        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email']
            user.save()

            # Hash the password with the set_password
            user.set_password(user.password)
            user.save()

            company = company_form.save(commit=False)
            company.user = user

            if 'picture' in request.FILES:
                company.picture = request.FILES['picture']

            company.save()

            user = authenticate(username=user_form.cleaned_data['email'],
                                password=user_form.cleaned_data['password'])

            login(request, user)
            return redirect('update_info')

        else:
            print user_form.errors, company_form.errors

    else:
        user_form = UserForm()
        company_form = CompanyForm()

    return render(request, 'account/register.html', {'user_form': user_form, 'company_form': company_form})


def update_info(request):
    if request.user.is_authenticated():
        company = request.user.company

        if request.method == 'POST':
            pass
        else:
            form = CompanyUpdateForm(initial={'description': company.description, 'website': company.website, 'location': company.location})

        return render(request, 'account/update_info.html', {'company': company, 'form': form})
    else:
        return redirect('register')


def company_logout(request):

    logout(request)

    return redirect('index')


def company_login(request):

    context = {}

    if request.user.is_authenticated():
        return redirect('update_info')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('update_info')

        else:
            context['issues'] = True

    return render(request, 'account/login.html', context)
