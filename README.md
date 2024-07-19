# test-app-lunch-place   
Greetings! This is a short test application where I developed a Lunch Place web app for an IT company. They can vote until a specified time. After the deadline, they can neither vote for lunch nor change their vote. After the deadline, they can neither place a new order nor change their vote.   
Users can choose only one lunch from the available restaurant menus, but they can change their vote if the voting period is still open. The menu changes daily, and from 00:00 AM, users have a new opportunity to choose their lunch.    
    
On the other hand, the web app features another type of user: the restaurant. Restaurants can post a menu for each day from Monday to Sunday, but only one menu per day. They can monitor voting results and, after a certain period, they will see the final results, helping them determine the number of lunches they need to prepare. Restaurants also have the ability to change or delete their menus.    
   
Tech Overview  
- Only Back End (without UI);    
- REST architecture;    
- Tech stack: Django + DRF, JWT, PostgreSQL, Docker(docker-compose), PyTests;     
- Added at least a few different tests;    
- README.md with a description of how to run the system;    
- flake8 and isort;    
- CI/CD(GitHub Actions);    
     
API FUNCTIONALITY:     
- Authentication     
  localhost:8888/api/register/(POST)    
  localhost:8888/api/login/(POST)    
  localhost:8888/api/logout/(POST)    
  localhost:8888/api/delete/(DELETE)    
- Functionality for authorized users  
  localhost:8888/api/menu/(POST, GET*)   
  localhost:8888/api/menu/<pk:id>/(PUT, DELETE, GET*)   
  localhost:8888/api/vote/<pk:id>/(POST, PUT)   
  localhost:8888/api/remove-vote/(DELETE)    
  localhost:8888/api/result/(GET)   
- Admin   
  localhost:8888/admin/(admin.site.urls from django.contrib)    
*(The GET method behaves differently for employees and restaurants, providing tailored responses based on the user type)     
