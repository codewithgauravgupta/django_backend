# Summary

We covered:

* Dev environment using Docker.

* django `models`, `migrations`, `views`, `viewsets`, `templates`, and `URL routing`.

* JSON Web Tokens (JWT) token-based authentication for user verification.

* Revoking JWT tokens: Logout endpoint to denylist tokens.

* Added caching.

* Create REST APIs using Django-Rest-Framework(DRF)

* Pytest for testing models and viewsets.

* Manual and Automatic Deployment on AWS using CI/CD pipeline using github workflows.

* serve the API and the React frontend over HTTPS using AWS CloudFront.

* Check Performance and query optimization having performant API with fewer SQL queries and faster API responses.

, and finally, security aspects.

# Setup Dev Environment

* open vscode

* create a debian dev container file using vscode with features of node, postgres, python and vscode extensions. Make sure we have `Node LTS`.

* npm install -g yarn

* Initialize Virtual env:
    python3 -m venv venv && source ./venv/bin/activate

* Create `app` folder and Initialize git repo

* Create `readme` and `.gitignore` and push to github.

* configure git:
    git config --global user.name "username"
    git config --global user.email "email@address.com"

* Install Dependencies:
    pip cache purge
    pip install --no-cache-dir -r requirements.txt
    pip install --upgrade pip

* Install React developer tools for browser

* Install HTTP request client Postman or Insomnia
    curl -o- "https://dl-cli.pstmn.io/install/linux64.sh" | sh
    tar -xzf Postman-linux-x64-<version>.tar.gz
    sudo mv Postman /opt
    sudo ln -s /opt/Postman/Postman /usr/bin/postman

    or

    https://insomnia.rest/download

* Setup AWS Account and EC2 Instance:
    https://portal.aws.amazon.com/billing/signup.%20If%20you%20don%E2%80%99t%20have%20an%20AWS%20account,%20you%20can%20still%20use%20any%20virtual%20private%20server%20(VPS)%20or%20virtual%20private%20cloud%20(VPC)%20you%20have%20online.%20However,%20we%20will%20also%20document%20how%20to%20create%20a%20VPC%20instance%20using%20AWS%20and%20how%20to%20upload%20the%20code%20and%20serve%20the%20Django%20API.

    In instance allow post 22, 8000 in security group of instance.

    ssh -i "django_backend_keys.pem" admin@ec2-13-238-194-209.ap-southeast-2.compute.amazonaws.com

* Create .env file at root of project on both local and ec2:
    SECRET_KEY=DEV_SECRET_KEY
    DJANGO_ALLOWED_HOSTS=*
    DB_NAME=coredb
    DB_USER=core
    DB_PASS=wCh29&HE&T83
    DB_HOST=localhost
    DB_PORT=5432
    CORS_ALLOWED_ORIGINS=http://49.36.27.211
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=postgres
    ENV=DEV

# Setup Django Project and app:

* Setup Django Project in jadngoProject directory after activating venv in djangoApp directory:

    `django-admin startproject root .`

* Create a core application that will hold all apps of django project.
    
    `django-admin startapp apps`

* Add label in class of apps in apps.py
   
    `label = 'apps'`

* Register apps in settings.py of root INSTALLED_APPS, using name field of apps.py of `apps`.

* Start Django Server:
    
    `python manage.py runserver 0.0.0.0:8000`

# Configure postgres on remote or local:

* Configure postgres container:
    docker exec -it 9393a6bd626d bash
    su postgres
    psql
    CREATE DATABASE coredb;
    CREATE USER core WITH PASSWORD 'wCh29&HE&T83';
    GRANT ALL PRIVILEGES ON DATABASE coredb TO core;
    GRANT ALL PRIVILEGES ON SCHEMA public TO core;
    ALTER ROLE core SUPERUSER;
    ALTER USER core CREATEDB;

* `Do not migrate`

* Connect to configured DB from settings.py:
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'coredb',
            'USER': 'core',
            'PASSWORD': 'wCh29&HE&T83',
            'HOST': 'db',
            'PORT': '5432',
        }
    }

    or

    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME", "coredb"),
        "USER": os.getenv("DB_USER", "core"),
        "PASSWORD": os.getenv("DB_PASS", "wCh29&HE&T83"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

# Create user app:

* Create user application under apps
    `cd apps && django-admin startapp user`

* Modify apps.py of user with label:
    name = "apps.user"
    label = "apps_user"

* Create user model in user models.py, The user table is as follows:
    public_id: string
    last_name: string
    first_name: string
    username: string
    bio: string
    avatar: image
    email: string
    is_active
    is_superuser
    created: datetime
    updated: datetime

* Moving on we will update it as for like feature:
    public id: string
    last_name: string
    first_name:string
    username: string
    bio: string
    avatar: image
    email: string
    post_liked: m2m
    author: FK<User>
    is_active
    is_superuser
    created: datetime
    updated: datetime

* Register user in settings.py, using name field of apps.py of user `"apps.user"`.

* We also need to tell Django to use this User model for the authentication user model. In the settings.py file add below at last line:
    AUTH_USER_MODEL = 'apps_user.User'

* Make Migrations:
    python manage.py makemigrations <app_name>
    python manage.py makemigrations apps_user

* Run Migrations:
    python manage.py migrate && python manage.py runserver 0.0.0.0:8000

* Test Migrations:
    python manage.py shell

    from apps.user.models import User

    data_user = {
        "email": "testuser@yopmail.com",
        "username": "john-doe",
        "password": "12345",
        "first_name": "John",
        "last_name": "Doe"
    }

    user = User.objects.create_user(**data_user)

    user.name

    user.email
    
    user.password

# Add Rest Framework to user app:

* Add rest_framework to installedapps:
    "rest_framework"
    "rest_framework_simplejwt",
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist",

* In settings file:
    CORS_ALLOW_ALL_ORIGINS = True
    or
    CORS_ALLOWED_ORIGINS = [
    'http://example.com',
    'https://example.com',
    ]

* Enable CORS:
    'corsheaders.middleware.CorsMiddleware', to middleware before common

    
* Create a serializers.py to create a UserSerializer in user app.

* Create viewset; Inside the user directory, rename the view file viewsets.py

* Define a router; At the root of the apps project (apps), create a file named routers.py.

* Modify root/urls.py for api route.

* make a GET request to http://0.0.0.0:8000/api/user/

* Make a patch request to http://0.0.0.0:8000/api/user/33d1969bd35f447fba39baf8a9543f89/
{
    "last_name": "Hey"
}

# Create auth app for register of users:

* Now that we are done with the user application, we can confidently move on to adding a login and user registration feature to the project, so that users can be authenticated to access the resources.

* If the registration of a user is successful, we will provide credentials, here JWTs, so the user won’t have to log in again to start a session—a win for user experience.

* Add to installed apps:
    'rest_framework_simplejwt',

    REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

* Creating the auth app, First, we need to write a registration serializer, but before that, let’s create a new application called auth in the apps application. It’ll contain all the logic concerning logging in, registration, logging out, and a lot more:

    cd apps && django-admin startapp auth

* rewrite apps.py for auth in installedapps

* Create a Python package called serializers and another one called viewsets in auth. Make sure that these new directories have an __init__.py file, with entries in it.
    from .register import RegisterSerializer

* Inside the serializers directory, create a file called register.py. It’ll contain the code for RegisterSerializer, which is the name of the registration serializer class.

* Next, we can add the viewset by creating a file register.py file in viewsets, also let’s register the viewset in the routers.py file.

* Test endpoint using HTTP Client:
    0.0.0.0:8000/api/auth/register/

    {
    "username": "mouse21",
    "first_name": "Mickey",
    "last_name": "Mouse",
    "password": "12345678",
    "email": "mouse@yopmail.com"
    }

    We will get two tokens.

* If we try sending same request we get a 400 error bad request, as the user already exists.

* we don’t need to revalidate fields such as email or password. Because we declared these fields with some conditions, Django will automatically handle their validation.

# auth Login and Referesh API for users:

* The next step is adding the login endpoint following the same process: writing the serializer and the viewset, and then registering the route.

* Using the djangorestframework-simplejwt package, which provides a serializer called TokenObtainPairSerializer, we’ll write a serializer to check for user authentication but also return a response containing access and refresh tokens. For this, we will rewrite the validate method from the TokenObtainPairSerializer class.

* Inside the apps/auth/serializers directory, create a new file called login.py (this file will contain LoginSerializer, a subclass of TokenObtainPairSerializer)

* We are surcharging the validate method from the TokenObtainPairSerializer class to adapt it to our needs. That’s why super is helpful here. It’s a built-in method in Python that returns a temporary object that can be used to access the class methods of the base class.

* Once the serializer is written, don’t forget to import it to the __init__.py file.

* The next step is to add the viewset. We’ll call this viewset LoginViewset. Because we are not directly interacting with a model here, we’ll just be using the viewsets.ViewSet class

* We can now import it and register it in the routers.py file.

* Test endpoint, The endpoint for login will be available at /auth/login/
    {
    "password": "12345678",
    "email": "mouse@yopmail.com"
    }

* However, right now the access token expires in 5 minutes. Basically, to get a new access token, the user will have to log in again. Let’s see how we can use the refresh token to request a new access token without logging in again.

* The command djangorestframework-simplejwt provides a refresh logic feature. As observed, we’ve been generating refresh tokens and returning them as responses every time registration or login is completed. We’ll just inherit the class from TokenRefreshView and transform it into a viewset.

* In auth/viewsets, add a new file called refresh.py and add the class in the __init__.py file and then register it in the routers.py file.

* Test endpoint /auth/refresh/ to get a new token, with refresh token as body.
    {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTM0MDEyMywiaWF0IjoxNzE1MjUzNzIzLCJqdGkiOiIyMzllNjAwZDRjN2I0OGEyYTRiNjNiNmUxNmJkMDQ4ZiIsInVzZXJfaWQiOjJ9.BMy28Aee4HL8UnAhgEjjjV4Gi5gdfSHWW8XUy21617o"
    }

    Refresh tokens are exchanged for new access tokens when the current access token expires, without needing the users to log in again and again. This allows continuous access to protected resources and enhances user experience.

# Optimize code using DRY by creating abstract classes for model, serializer and viewsets.

* Lets follow DRY, The DRY(Dont Repeat Yourself) principle is a best practice in software development that encourages software developers to avoid repetition of instructions. We will create a abstract model class, as we will create many models that will have similar fields.

* Inside the `apps` directory, create a new Python package called `abstract`. Once it’s done, create a `models.py` file. In this file, we will write two classes: `AbstractModel` and `AbstractManager`.

* The `AbstractModel` class will contain fields such as `public_id`, `created`, and `updated`. On the other side, the `AbstractManager` class will contain the `function used to retrieve an object by its public_id field`

* As we can see in the Meta class for `AbstractModel`, the abstract attribute is set to `True`. `Django will ignore this class model` and won’t generate migrations for this.

* let’s make a quick `refactor on the User model`: First, let’s `remove the get_object_by_public_id` method to retrieve an object via `public_id`, and let’s subclass `UserManager`.

* On the User model, we’ll remove the `public_id`, `updated`, and `created` fields and subclass the User model with the AbstractModel class. This will normally cause no changes to the database—therefore, there is `no need to run makemigrations` again `unless we’ve changed an attribute of a field`.

* Let’s also add `AbstractSerializer`, which will be used by all the `serializers` we’ll be creating on this project.

* All the `objects sent back as a response in our API will contain the id, created, and updated fields`. It’ll be repetitive to write these fields all over again on every ModelSerializer, so let’s just `create an AbstractSerializer class`. In the abstract directory, `create a file called serializers.py`.

* Once it’s done, we can go and `subclass the UserSerializer class with the AbstractSerializer class`, Once it’s done, we’ll `remove the field declaration of id, created, and updated`.

* one last `abstraction for ViewSets`, But why write an abstract ViewSet? Well, there will be repeated declarations as to the `ordering and the filtering`. Let’s create a class that will contain the default values. In the abstract directory, `create a file called viewsets.py`

* The next step is to add the `AbstractViewSet class to the code where ModelViewSets` is actually called. Go to `apps/user/viewsets.py` and `subclass UserViewSet with the AbstractViewSet class`.

# Create post app

* Till now, we used models, serializers, viewsets, and routes to create our first endpoints.

* Lets create a social-media post app, where A post in this project is a long or short piece of text that can be viewed by anyone, irrespective of whether a user is linked or associated to that post.

* Here are the requirements for the post feature:

    Authenticated users should be able to create a post.
    Authenticated users should be able to like the post.
    All users should be able to read the post, even if they aren’t autherized.
    The author of the post should be able to modify the post.
    The author of the post should be able to delete the post.

* we’ll be dealing with a database, a model, and permissions.

* The foreign key is one of the characteristics of the one-to-many (or many-to-one) relationship. In this relationship, a row in table A can have many matching rows in table B (one-to-many), but a row in table B can only have one matching row in table A.

* In our case, a user (from the User table) can have many posts (in the Post table) but a post can only have one user. The many-to-many relationship will be used when writing the like feature for the posts.

* Now lets create post app:
    `django-admin startapp post`

* Rewrite apps.py of the new create package so it can be called easily in the project.

* Create Post Model, there is an author field, which is a foreign key. A foreign key is a set of attributes in a table that refers to the primary key of another table. In our case, the foreign key will refer to the primary key of the User table. Each time a post is created, a foreign key will need to be passed.

* Post Table Fields:
    public id: string
    author: FK<User>
    body: string
    edited: boolean
    created: datetime
    updated: datetime

*  Django models actually provide tools to handle this kind of relationship. It’s also symmetrical, meaning that not only can we use the Post.author syntax to access the user object but we can also access posts created by a user using the User.post_set syntax. The latter syntax will return a queryset object containing the posts created by the user because we are in a ForeignKey relationship, which is also a one-to-many relationship. You will also notice the on_delete attribute with the models.CASCADE value. Using CASCADE, if a user is deleted from the database, Django will also delete all records of posts in relation to this user.

Apart from CASCADE as a value for the on_delete attribute on a ForeignKey relationship, we can also have the following:

SET_NULL: This will set the child object foreign key to null on delete. For example, if a user is deleted from the database, the value of the author field of the posts in relation to this user is set to None.

SET_DEFAULT: This will set the child object to the default value given while writing the model. It works if you are sure that the default value won’t be deleted.

RESTRICT: This raises the RestrictedError under certain conditions.

PROTECT: This prevents the foreign key object from being deleted as long as there are objects linked to the foreign key object.

* Add the newly created application to the INSTALLED_APPS list

* python manage.py makemigrations && python manage.py migrate

* Let’s test the newly added model by creating an object and saving it in the database:
    python manage.py shell or use django_shell_plus to avoid manual imports.

    from apps.post.models import Post
    from apps.user.models import User
    user = User.objects.first()
    user

* let’s create a dictionary that will contain all the fields needed to create a post:

    data = {"author": user, "body":"A simple test"}

let’s create a post:

    post = Post.objects.create(**data)
    post.author
    user.post_set.all()

* the post_set attribute contains all the instructions needed to interact with all the posts linked to this user.

* writing the `serializer of the Post object`: The Post serializer will contain the fields needed to create a post when making a request on the endpoint. Let’s add the feature for the post creation first. In the post directory, create a file called `serializers.py`. 

* We’ve added a new serializer field type, SlugRelatedField. As we are working with the ModelSerializer class, Django automatically handles the fields and relationship generation for us. Defining the type of relationship field we want to use can also be crucial for telling Django exactly what to do.

And that’s where SlugRelatedField comes in. It is used to represent the target of the relationship using a field on the target. Therefore, when creating a post, the public_id of the author will be passed in the body of the request so that the user can be identified and linked to the post.

The validate_author method checks validation for the author field. Here, we want to make sure that the user creating the post is the same user as in the author field. A context dictionary is available in every serializer. It usually contains the request object that we can use to make some checks.

* Writing Post Viewsets, For the following endpoint, we’ll only be allowing the POST and GET methods. This will help us have the basic features working first. The code should follow these rules:

    Only authenticated users can create posts.

    Only authenticated users can read posts.

    Only GET and POST methods are allowed.

* Inside the post directory, create a file called viewsets.py. 

* The get_queryset method returns all the posts. We don’t actually have particular requirements for fetching posts, so we can return all posts in the database.

The get_object method returns a post object using public_id that will be present in the URL. We retrieve this parameter from the self.kwargs directory.

The create method, which is the ViewSet action executed on POST requests on the endpoint linked to ViewSet. We simply pass the data to the serializer declared on ViewSet, validate the data, and then call the perform_create method to create a post object. This method will automatically handle the creation of a post object by calling the Serializer.create method, which will trigger the creation of a post object in the database. Finally, we return a response with the newly created post.

* Adding the Post route#

* Test endpoint, Creating a sample post# /post/
    Get: http://0.0.0.0:8000/api/post/

    use bearer token from /login

    {
        "author": "fb2d39265992477da9e437335835a6a9",
        "body": "A simple post"
    }

* Actually, the author field accepts public_id and returns public_id. While it does the work, it can be a little bit difficult to identify the user. This will cause it to make a request again with the public_id of the user to get the pieces of information about the user.

The to_representation() method takes the object instance that requires serialization and returns a primitive representation. This usually means returning a structure of built-in Python datatypes. The exact types that can be handled depend on the render classes you configure for your API.

As you can see, we are using the public_id field to retrieve the user and then serialize the User object with UserSerializer.

# Configure Authorization i.e. permissions: 

* Create a superuser: 
    `python manage.py createsuperuser --username admin --email admin@example.com`

* If authentication is the action of verifying the identity of a user, authorization is simply the action of checking whether the user has the rights or privileges to perform an action.

* we hve three types of users, anonymous user, registered, admin. we need to write a custom permission.

* Django permissions usually work on two levels: on the overall endpoint (has_permission) and on an object level (has_object_permission).

A great way to write permissions is to always deny by default; that is why we always return False at the end of each permission method. We can then start adding the conditions. Here, in all the methods, we are checking that anonymous users can only make the SAFE_METHODS requests—GET, OPTIONS, and HEAD.

For other users, we are making sure that they are always authenticated before continuing.

* Inside the `auth` directory, create a file called `permissions.py`.

* Next Allow users to update and delete posts. 

* To add these functionalities, we don’t need to write a serializer or a viewset, because the methods for deletion (destroy()), and updating (update()) are already available by default in the ViewSet class. 

* We will just rewrite the update method on PostSerializer to ensure that the edited field is set to True when modifying a post.

* Let’s add the PUT and DELETE methods to http_methods of PostViewSet

* Also modify the serializer for post.

* Test updating and deleting the post after login:
    http://0.0.0.0:8000/api/post/176fade8f90444719b14b0c9eac3a540/
    {
    "author": "fb2d39265992477da9e437335835a6a9",
    "body": "A simple post edited"
    }

Note: There is a way to delete records without necessarily deleting them from the database. It’s usually called a soft delete. The record just won’t be accessible to the user, but it will always be present in the database.

# Adding Like Feature to posts:

* Adding Like Feature:
    Add a new posts_liked field to the User model.

    Write methods on the User model to like and remove a like from a post.  We’ll also add a method to check whether the user has liked a post.

    Add likes_count and has_liked to PostSerializer.

    Add endpoints to like a post and remove a like from a post.

* The posts_liked field will contain all the posts liked by a user. The relationship between the User model and the Post model concerning the “Like” feature is many-to-many.

* Open the /apps/user/models.py file and add a new field to the User model

* Inside the apps/post/serializers.py file, add new fields to PostSerializer

* Adding endpoints like and remove like actions to PostViewSet.

* For each action added, we are writing the logic following these steps:

First, we retrieve the concerned post on which we want to call the like or remove the like action. The self.get_object() method will automatically return the concerned post using the ID passed to the URL request, thanks to the detail attribute being set to True.

Second, we also retrieve the user making the request from the self.request object. This is done so that we can call the remove_like or like method added to the User model.

And finally, we serialize the post using the Serializer class defined on self.serializer_class and we return a response.

With this added to PostViewSets, the Django Rest Framework routers will automatically create new routes for this resource.

* makemigrations and migrate

* Test Endpoints, post_pk is post id.

    Like a post: api/post/post_pk/like/
    Remove Like: api/post/post_pk/remove_like/

    http://0.0.0.0:8000/api/post/a795d4d1f7524b4faf0ee37e174914ea/like/
    http://0.0.0.0:8000/api/post/a795d4d1f7524b4faf0ee37e174914ea/remove_like/

# Create comment app, to add and delete comments to our posts:

A comment in the context of this project will represent short text that can be viewed by anyone but only be created or updated by authenticated users.

    Any user can read comments.

    Authenticated users can create comments under posts.

    The comment author and post author can delete comments.

    The comment author can update posts.

* Create comment app

* Writing the Comment model.
    public_id: string
    body: string
    author: FK
    post: FK
    edited: boolean
    created: datetime
    updated: datetime

    A comment will mostly have four important fields: the author of the comment, the post on which the comment has been made, the body of the comment, and the edited field to track whether the comment has been edited or not.

    the author (User) and post (Post) fields are ForeignKey types. This relates to some rules for the comment feature:

    * A user can have many comments, but a comment is created by one user.

    * A post can have many comments, but a comment is linked to only one post.

* makemigrations and migrate

* Write comment model based on comment table and Test shell: 
    python manage.py shell
    from apps.comment.models import Comment
    from apps.post.models import Post
    from apps.user.models import User
    user = User.objects.first()
    post = Post.objects.first()
    comment_data = {"post": post, "author": user, "body": "A comment."}
    comment = Comment.objects.create(**comment_data)
    comment
    comment.body

* now that we are sure that the comment is working, we can write the serializer for the comment feature. 

* Now write endpoints using viewsets.    Writing the CommentViewSet class.

* Nesting routes for the comment resource.

* Add permissions in permissions.py

* Test endpoint 
    /api/post/post_pk/comment/comment_pk to create comments.

    {
    "author": "fb2d39265992477da9e437335835a6a9",
    "body": "Hey! I like your post.",
    "post": ""a795d4d1f7524b4faf0ee37e174914ea""
    }

* Test update and delete comment using PUT and DELETE: 
    /api/post/post_pk/comment/comment_pk/

    {
    "author": "fb2d39265992477da9e437335835a6a9",
    "body": "A simple comment edited",
    "post": ""a795d4d1f7524b4faf0ee37e174914ea""
    }    

# Testing Rest APIs:

* Testing Application using pytest; Create a file pytest.ini at root of project, i.e. where manage.py is present.

* run command to check if pytest is configured.
    /django_app/pytest

* Create first test by creating file tests.py at root.

* Run run pytest:
    /django_app/pytest

* Lets write test for django models, by creating `tests.py` inside apps/user.

* For testing post, we will need to create a fixture that will provide user data to post. Create a package `fixtures` in apps. We will have a user fixture by creating `user.py` under `fixtures` directory.

* Inside the core/post directory, create a new file called tests.py. This file will then test for the creation of a post.

* Writing tests for the Comment model requires the same steps as the tests for the Post model. First of all, create a new file called `post.py` in the apps/fixtures directory.

* Lets write test for django viewsets, CReate  conftest.py at root to create an API client using fixture.

* Inside the apps/auth directory, create a file named tests.py. Instead of writing test functions directly, we write a class that will contain the testing methods

* Lets Refactor code a bit, Inside the apps/post directory, we’ll create a Python package called tests. Once it’s done, we’ll rename the tests.py file in the apps/post directory to `test_models.py` and move it to the core/post/tests/ directory. 

* Inside the same directory, we create a new file called test_viewsets.py. This file will contain tests for PostViewSet.

* Do the same with comment, user, auth etc.

# Add Logout endpoint:

Add `"rest_framework_simplejwt.token_blacklist",` to installed apps.

Create a file called `logout.py` in the `apps/auth/viewsets` directory. This file will contain the code for the viewsets and the logic to denylist a token.

The logout endpoint will only accept POST requests, because the client will be required to pass a refresh token within the body of the POST request. We also specify that only authenticated users have permission to access this endpoint.

Add the newly created ViewSet in the `routers.py` file and register a new route

add a test for the newly added route in the `core/auth/tests/test_viewsets.py` file

change permissions in `permissions.py` in `auth`.

Run tests using `pytest` or `docker-compose exec -T api pytest`

# Add Caching

Implement caching in the Django application for optimized data retrieval.

Check service status `service redis-server status`, in dev container or in docker.

CACHES setting in the settings.py file.

Caching depends a lot on the business requirements for how much time you want to cache the data. Django provides many levels for caching:

* Per-site cache: This enables us to cache our entire website.

* Template fragment cache: This enables us to cache some components of the website. For example, we can decide to only cache the footer.

* Per-view cache: This enables us to cache the output of individual views.

* Low-level cache: Django provides an API we can use for interacting directly with the cache. It is useful if we want to produce a certain behavior based on a set of actions. For example, in this course, if a post is updated or deleted, we will update the cache.

Our requirement is if there is a delete or an update on a comment or a post, the cache is updated. Otherwise, we return the same information in the cache to the user.

This can be achieved in many ways. We can use Django signals or directly add custom methods to the manager of the model’s Post and Comment classes. Let’s go with the latter. 

We will surcharge the save and delete methods of the AbstractModel class, so if there is an update on a Post or Comment object, we update the cache.

Inside the apps/abstract/models.py file, add the following method on top of the file after the imports:

```python
from django.core.cache import cache
...
def _delete_cached_objects(app_label):
 if app_label == "core_post":
 cache.delete("post_objects")
 elif app_label == "core_comment":
 cache.delete("comment_objects")
 else:
 raise NotImplementedError
```
The function in the preceding code takes an application label, and according to the value of this app_label, we invalidate the corresponding cache. For the moment, we only support caching for posts and comments. Notice how the name of the function is prefixed with a _. This is a coding convention to specify that this method is private and should not be used outside the file where it is declared.

Inside the AbstractModel class, we can surcharge the save method. Before the save method is executed, we invalidate the cache. This means that on operations such as create and update, the cache will be reset:
```python
class AbstractModel(models.Model):
...
 def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        app_label = self._meta.app_label
        if app_label in ["core_post", "core_comment"]:
            _delete_cached_objects(app_label)
        return super(AbstractModel, self).save(force_insert=force_insert,force_update=force_update,using=using,update_fields=update_fields)
```
In the preceding code, we retrieve app_label from the _meta attribute on the model. If it corresponds to either core_post or core_comment, we invalidate the cache, and the rest of the instructions can proceed. Let’s do the same for the delete method:

```python
class AbstractModel(models.Model):
…
 def delete(self, using=None, keep_parents=False):
        app_label = self._meta.app_label
        if app_label in ["core_post", "core_comment"]:
            _delete_cached_objects(app_label)
        return super(AbstractModel, self).delete(using=using, keep_parents=keep_parents)
```

The cache invalidation logic has been implemented on the models. Let’s add the logic for cache data retrieving on the viewsets of the core_post application and the core_comment application.

`Retrieving data from the cache`:

The cache invalidation is ready, so we can freely retrieve data from the cache on the endpoints for the posts and the comments. 

Inside the PostViewSet class, we will rewrite the list() method. On the Django REST framework (DRF) open-source repository, the code looks like this:

```python
"""List a queryset"""
def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)
```
In the preceding code, a queryset call is made to retrieve the data, and then this queryset call is paginated, serialized, and returned inside a Response object. Let’s tweak the method a little bit:

```python
def list(self, request, *args, **kwargs):
    post_objects = cache.get("post_objects")
    if post_objects is None:
        post_objects = self.filter_queryset(self.get_queryset())
        cache.set("post_objects", post_objects)
    page = self.paginate_queryset(post_objects)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    serializer = self.get_serializer(post_objects, many=True)
    return Response(serializer.data)
```
In the preceding code, instead of doing a lookup on the database directly, we check the cache. If post_objects is None when making a query to the database, save queryset in the cache and finally proceed to return the cache objects to the user.

As you can see, the process is very simple. We just need to have a robust caching strategy. You can do the same for CommentViewSet

# optimize the backend build using webpack:

search on internet see if this is possible.

# Secure the full stack application over HTTPS using AWS CloudFront.

# Deployment to AWS:

    How do we make changes to our code and make deployment and testing automatic

    deploy Django app on EC2 and react on aws s3 or vercel
    
    security and performance optimizations

* Deploy django on aws:
    chmod 400 "django_backend_keys.pem"
    ssh -i django_backend_keys.pem admin@ipaddress
    ssh -i "django_backend_keys.pem" admin@ec2-13-210-241-10.ap-southeast-2.compute.amazonaws.com
    sudo apt update
    sudo apt upgrade

    The Django project will run on port 8000 on the machine, so we have to allow a connection to this port. By default, EC2 instances will only allow connections on ports 80 for HTTP requests, 22 for SSH connections, and—sometimes—443 for Secure Sockets Layer (SSL) connections.

    You can allow connections on port 8000 directly. On the “Details” page of the created EC2 instance, go to the “Security” tab on the list of tabs at the bottom of the page and click the security setting group:

* Automatic django app deployment using github actions.

* Workflow files are stored in a dedicated directory called .github/workflows.

* At the root of the project, we’ll create a directory called .github, and inside this directory, we’ll create another directory called workflows. Inside the workflows directory, we’ll create a file called ci-cd.yml.

* Build is success but without test check once.

* On Local Machine:

    Get the pem file from aws and store in non-ntfs and change permission to 400
    
    ssh -i "django_backend_keys.pem" admin@ec2-13-210-241-10.ap-southeast-2.compute.amazonaws.com

    ssh-keygen -t rsa -b 4096 -C "gglearnpractice@gmail.com"

    copy the content of the public key and add it to the .ssh/authorized_keys file of the remote EC2 instance. 

    sudo cat /home/dev/.ssh/id_rsa.pub | ssh -i "django_backend_keys.pem" admin@ec2-13-210-241-10.ap-southeast-2.compute.amazonaws.com 'cat >> .ssh/authorized_keys'

    Then, copy the content of the private key and add it to GitHub Secrets:

* Create docker-ec2-deploy.sh

* chmod +x docker-ec2-deploy.sh


optional at last:
cd usercode/django-api/ && cp -r runserver.py /usr/local/lib/python3.10/dist-packages/django/core/management/commands/runserver.py  && service postgresql start &&  python manage.py makemigrations && python manage.py migrate && python manage.py runserver > /dev/null 2>&1 &

# DB Migration Issue (Migration admin.0001_initial is applied before its dependency core_user.0001_initial on database 'default'.):

* python manage.py showmigrations

* su postgres -> psql

* Terminate all psql connection if error in above step:
    SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'coredb' AND pid <> pg_backend_pid();

* drop database coredb; -> CREATE DATABASE coredb;

$ sudo su postgres
$  psql
postgres=# DROP DATABASE coredb;
postgres=# CREATE DATABASE coredb;
postgres=# ALTER ROLE core SET client_encoding TO 'utf8';
postgres=# ALTER ROLE core SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE core SET timezone TO 'UTC';
postgres=# ALTER DATABASE coredb OWNER TO core;
postgres=# GRANT ALL PRIVILEGES ON DATABASE coredb TO core;

# Restart Postgresql in dev container:

service postgresql --full-restart