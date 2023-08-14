from django.shortcuts import render, redirect

from django import forms

from django.http import HttpResponse # new 

from django.views.generic import TemplateView 

from django.views import View 

# Create your views here. 

def homePageView(request): # new 

    return HttpResponse('Hello World!') # new 

class HomePageView(TemplateView): 

    template_name = "pages/home.html"

class AboutPageView(TemplateView):
  template_name = 'pages/about.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
        "title": "About us - Online Store",
        "subtitle": "About us",
        "description": "This is an about page ...",
        "author": "Developed by: Yhilmar Chaverra",
    })

    return context

class Product: 
   products = [
      {"id":"1", "name":"TV", "description":"Best TV", "price": 150},
      {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 300},
      {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 500},
      {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 200},
  ]

class ProductIndexView(View): 

    template_name = 'products/index.html' 

    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 

        return render(request, self.template_name, viewData) 


class ProductShowView(View):

  template_name = 'products/show.html'

  def get(self, request, id):
    viewData = {}
  
    try:
        product_id = int(id)
        product = next((p for p in Product.products if int(p['id']) == product_id), None)

        if product is None:
            return redirect("home")  # Redirect to the home page if product is not found
        
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        viewData["price"] = product["price"]

        return render(request, self.template_name, viewData)
    except ValueError:
        return redirect("home")


class ProductForm(forms.Form):
  name = forms.CharField(required=True)
  price = forms.FloatField(required=True)

  def clean_price(self):
    price = self.cleaned_data['price']
    if price <= 0:
        raise forms.ValidationError("The price must be greater than 0")
    return price
  

class ProductCreateView(View):

  template_name = 'products/create.html'

  def get(self, request):
      form = ProductForm()
      viewData = {}
      viewData["title"] = "Create product"
      viewData["form"] = form
      return render(request, self.template_name, viewData)

  def post(self, request):
      form = ProductForm(request.POST)
      if form.is_valid():
          success_message = "Product created"
          form = ProductForm()  
          viewData = {"title": "Create product", "form": form, "success_message": success_message}
          return render(request, self.template_name, viewData)
      else:
          viewData = {}
          viewData["title"] = "Create product"
          viewData["form"] = form
          return render(request, self.template_name, viewData)