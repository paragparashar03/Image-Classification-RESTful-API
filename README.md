# Image-Classification-RESTful-API
Image Classification RESTful-API is a FLASK based API. Inception V3 model has been used to classify Images.
But it can basically classify animals, plants, humans, famous people, airplanes. etc in an Image. We will be giving url of the image which we want to classify and the model will generate different classes and their respective probabilities to categorize the given Image. 

MOTIVATION:
This is an API aimed at exploring FLASK, databases as a service (MongoDb), and RESTful APIs on the Ubuntu platform.
We dockerized this appplication and deployed it in the web.

NOTES:
1. Classify_image.py file (in web folder) contains the model for classification (downloaded from github). You can import new classification models as well.
2. app.py is the main file for this application.
3. We have docker-compose.yml file and 2 folders
   1. db (that has a Dockerfile for mongodb) 2. web (that has app.py, classify_image.py, Dockerfile, requirement.txt files)

4. docker-compose.yml file controls the application.

5. You gave to build the application first. On terminal write:  
   sudo docker-compose build
   sudo docker-compose up
   
6. You will get url after succesfully running above commands. Paste that url on the POSTMAN to control things
7. POSTMAN is used to send/receive (POST/GET) request/responses.
8. classify_image.py file uses tensorflow v1. So, I have used Python:3.6.7 in the Dockerfile so that tensorflow 1.14 is installed when we dockerize the application.
9. See requirement.txt file to the redependencies for the present application.




.








