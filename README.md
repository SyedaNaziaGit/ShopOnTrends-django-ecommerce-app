# Shop On Trends

## A Django Ecommerce Application

### About Project

Designed and developed a comprehensive e-commerce web application using Django, featuring:
- Robust order management systems with CRUD operations
- Product catalog management with high-quality image uploads and detailed product pages
- User authentication and authorization with login, registration, and logout functionality
- Search bar with category filtering and sorting capabilities
- Dedicated About page for brand storytelling
- Shopping cart model with add-to-cart functionality and dynamic pricing updates
- Secure payment gateway integration with PayPal
  
### 1.  Demo URL  - 

http://127.0.0.1:8000/

![image](https://github.com/user-attachments/assets/9fb51420-9eb9-491a-829d-e21813d27d12)

### 2.  Admin portal -

http://localhost:8000/admin/

![image](https://github.com/user-attachments/assets/ad945832-87a1-4e71-a476-4bababc801bf)


### 3.  Tech Stack Used:

- Python , Django, HTML , CSS, Javascript , PostgresSQL ,ngrok for testing

  please refer requirements.txt in the code for the libraries used
  
### 4.  High Level Functionality

Shop On trends is an ecommerece web application used developed for shopping all the trendy stuff in  the society. Here the application is micro managed with the advantage of django structure as it is loosely coupled.
We have ecomm project app which includes apps like store , shopping cart, payment .Store app has all the product,product categories, product page ,CRUD operations ,Authentication and Authorization and search of products ,
whereas Shopping Cart has cart summary total and discounts if included, and Payment app has Order summary, billing information, payment shipped, for the admin if the orders are shipped or delayed.
So tried my best to build a functional ecommerce application.

### 5. Process of Building Shop On Trends Application in Django -

Follow these steps :

- install the requirements.txt 

- creating an virtual environment

  pip install venv

  python -m venv virtual_env_name

- check for python version

  python -V

  pip install django

- create django project

  django-admin startproject projectname

- create app inside the project where manage.py is visible

python manage.py startapp appname

add app in settings.py

- Runserver : this  will run on localhost:8000

python manage.py runserver

- Getting admin page access:

  python manage.py makemigrations

  python manage.py migrate

  -create user - login to admin

  python manage.py createsuperuser

give username and password and login to localhost:8000/admin

- After creating any models make migrations and register the model in admin.py

admin.model.register(ModelName)

- Add Media and static path in settings.py and urlpatterns


### 6.  Screenshots Related to application

1. Login Page


<img width="814" alt="image" src="https://github.com/user-attachments/assets/c6244a85-bf0b-4902-b20b-7be0cd36555b">


2. Register Page


<img width="740" alt="image" src="https://github.com/user-attachments/assets/ab8dd384-693d-4fef-a753-55b7551afa1f">


3. Product Page with Id slug:


<img width="800" alt="image" src="https://github.com/user-attachments/assets/55679307-8395-4255-8f33-0523fef2989a">


4. Shopping Cart Page:


<img width="818" alt="image" src="https://github.com/user-attachments/assets/36e26754-2fa3-41a4-92d3-42c040b39770">


5. Checkout page:


<img width="812" alt="image" src="https://github.com/user-attachments/assets/20b1a5b5-1fc6-48b5-ae84-c2f1d9fca260">


6. Billing Information Page:

<img width="542" alt="image" src="https://github.com/user-attachments/assets/8058b152-5ae1-4b8d-b96b-121cf319911e">
      

7.  For the SuperUsers or the admin pannel can check for orders shipped or not


<img width="751" alt="image" src="https://github.com/user-attachments/assets/37a120a8-0dd7-45fe-b5ea-77ab920e48d4">


8. Shipped and non shipped items are visible in table along with id and id is accessible to product


<img width="717" alt="image" src="https://github.com/user-attachments/assets/cefa23f0-4ce6-407f-a9d4-720d3fe48ea6">


9. Category summary has all the categories in the database:


<img width="722" alt="image" src="https://github.com/user-attachments/assets/7717dbe8-5bae-485e-9c21-55dd1a0642ec">


10. Search Page:


<img width="689" alt="image" src="https://github.com/user-attachments/assets/f837ba05-03eb-49fd-98a6-6a70b5bc943d">


11. Update User Profile:


<img width="575" alt="image" src="https://github.com/user-attachments/assets/206a8184-7501-4999-b0d8-edb89ef02fe4">


### Resources Used:

1. https://getbootstrap.com/docs/5.3/getting-started/introduction/

2. https://docs.djangoproject.com/en/5.1/
 


