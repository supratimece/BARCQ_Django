from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import JsonResponse
import json
#from json_field import JSONField
# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
#from .pythonBackend import jsonCodeGenerator

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)

			Customer.objects.create(
				user=user,
				name=user.username,
			)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'frontend/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'frontend/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'frontend/dashboard.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()
	savedcircuits = request.user.customer.savedcircuit_set.all()
	
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	filename=request.user.customer.savedcircuit_set.all().values_list('name', flat=True)
	print(filename)
	context = {'orders':orders,'total_orders':total_orders, 
	'delivered':delivered,'pending':pending, 'savedcircuits': savedcircuits, 'filename':filename}
	return render(request, 'frontend/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	return render(request, 'frontend/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()
	saved_circuit = customer.savedcircuit_set.all()
	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'frontend/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'frontend/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'frontend/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'frontend/delete.html', context)


def CodeGenerator(request):
	if request.method == "POST":
		print("====================================")
		print("data received by django")
		data = request.body.decode("utf-8")
		print(data)
		#savedcircuit = SavedCircuit()
		#savedcircuit.circuit=data
		#print(savedcircuit.circuit)
		#result =  jsonCodeGenerator(data)
		#print(result)
		#return JsonResponse(result,safe=False)
		return JsonResponse(data,safe=False)
		# return render(request, 'frontend/user.html')
	else:
		print("** NOT POST****")
		return render(request, 'frontend/user.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def SaveCircuit(request, pk=None):
	if request.method == "POST":
		print("====================================")
		print("Request received for saving")
		data = request.body.decode("utf-8")
		# print(data)
		#data_dict = json.loads(data)
		filename = request.POST['filename']
		circuit = request.POST['circuit_data']
		# print(filename)
		# print(circuit)
		user = request.user
		# print("***********",user,"********")
		customer = Customer.objects.get(user=user)
		# print(customer)
		saved_circuit = SavedCircuit(customer=customer, circuit=circuit, name=filename)
		saved_circuit.save()

		#request.user.customer.savedcircuit.circuit=data
		print("******data saved*****")
		return JsonResponse(filename, safe=False)

	else:
		print("** NOT SAVED****")
		return render(request, 'frontend/user.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def loadCircuit(request, pk=None):
	if request.method == "POST":
		print("====================================")
		print("Request received for loading")
		
		return redirect('/')
	else:
		print("** NOT SAVED****")
		return render(request, 'frontend/user.html')

def deleteCircuit(request, pk):
	savedcircuits = SavedCircuit.objects.get(id=pk)
	# if request.method == "POST":
	savedcircuits.delete()
	return redirect('/')

	# context = {'savedcircuits':savedcircuits}
	# return render(request, 'frontend/user.html', context)

def helpPage(request):

	return render(request, 'frontend/help.html')