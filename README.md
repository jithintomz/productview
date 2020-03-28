# ProductView
A project to manage product uploads of acme Inc
=========================

Technologies Used
------------
1.Django - Webframework. 
2.Celery - Asynchonous Tasks. 
3.Angulrjs - Frontend Mvc. 
4.Postgres - Database. 
5.Nginx - Production Server. 
6.django-channels - Server Side events  


Basic Architecture
------------
1.The uploaded file is saved to the local server file system and response is sent to user. 
2.A celery task is initiated to parse records from the csv and save it to the database in chunks. 
3.User is updated about the status of parsing and processing through websockets. 
4.Users are allowed to add webhooks which are used to notify in case of product updates asynchronously. 
with few retries

ToDo
------------
1.Better and more notifications at frontend.  
