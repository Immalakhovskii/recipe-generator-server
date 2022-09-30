# Recipe Maker: Foodgram (Server Edition) #
*For a while this project will be available online via remote server, but after a suspension of a virtual machine only local version of the project will be operable. Check it out here: https://github.com/Immalakhovskii/recipe-generator-local*

---
#### Technology Stack ####
Python 3.7 / Django 2.2.19 / Django REST framework 3.13.1 / PostgreSQL 13.0 / Djoser 2.1.0 / Docker 20.10.17 / Node.js 13.12.0 (used in prearranged frontend made with React)
#### Description ####
Foodgram is a site that stores, shows and filters recipes from different authors. Via Foodgram users can create their own recipes with text description, single image, ingredients with amount. Ingreients preadded into database, list of ingredients can be expanded in admin zone. Every recipe has tags which are useful for filtering and brief insight on recipe features. All authorized users can subscribe to authors, add recipes to favorites and add recipes to shopping cart. Shopping cart can be downloaded as pdf shopping list which summarizes amounts of equal ingredients and shows total amount. See full API documentation here: http://foodgramm.sytes.net/api/docs/
#### Try it out ####
Foodgram available at: http://foodgramm.sytes.net/, admin zone: http://foodgramm.sytes.net/admin/   
```
# access site and admin zone as Admin superuser
email: adminmail@mail.com
password: youllneverguess

# access site as regular user Pasha
email: somemail5@mail.com
password: youllneverguess
```
#### GitHub Actions ####
On every push the project passes Flake8 tests and new version of backend Docker image pushes to Docker Hub. Final action is an automatic deploy of the project to private virtual machine