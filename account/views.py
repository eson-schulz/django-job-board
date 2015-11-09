from django.shortcuts import render
from .forms import CompanyForm, UserForm


def register(request):

    registered = False

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

            registered = True

        else:
            print user_form.errors, company_form.errors

    else:
        user_form = UserForm()
        company_form = CompanyForm()

    return render(request, 'account/register.html', {'user_form': user_form, 'company_form': company_form, 'registered': registered})


def update_info(request):

    return render(request, 'account/update_info.html')