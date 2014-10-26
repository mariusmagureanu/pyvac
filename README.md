Pyvac is a noob python project meant to interact with Varnish environment. Specifically it will directly rely on varnish agent instances in order to control varnish caches.

# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
  Pyvac runs on top of MongoDB and Flask, make sure you have mongo up and running with its default settings, 
  flask on the other hand will automatically be installed when running <i>fab install</i>.
  
* Version
  0.1
  
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
  Run <i>sudo fab install</i>
  If the installation has been succesfull, open a terminal and type <i>vac</i>.
  
* Configuration
  Mongo runs on its default settings, no changes required here.
  Flask will start running on port 8182 when starting the shell, you can test that flask is up and running by issuing this in your browser: 
  http://localhost:8182/test
  
* Dependencies
  All dependencies are fetched by <i>fab install</i>
  
* Database configuration
  None required.
  
* How to run tests
  Run <i>fab test</i> in pyvac's root folder. It will run both unit tests and pep8.
  
* Deployment instructions

### Contribution guidelines ###

* Writing tests
  Add your tests under /vac/test/
* Code review
  Any code in pyvac should comply the pep8 standard. Run <i>fab test</i> to check your code.
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact