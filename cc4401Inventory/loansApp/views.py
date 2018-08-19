from django.shortcuts import render
from .models import Loan
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def loan_data(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        user = request.user

        context = {
            'loan': loan,
            'user': user
        }

        return render(request, 'loan_data.html', context)

    except Exception as e:
        print(e)
        return redirect('/')

@login_required
def lost_request(request, loan_id):
    if request.method == 'POST':
        loan = Loan.objects.get(id=loan_id)
        loan.state = "Pe"
        loan.article.state = "L"
        loan.save()
        loan.article.save()
        return redirect('/')

@login_required
def cancel_request(request, loan_id):
    if request.method == 'POST':
        loan = Loan.objects.get(id=loan_id)
        loan.delete()
        return redirect('landing_articles')