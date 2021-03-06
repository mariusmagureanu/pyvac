Pyvac is a noob python project meant to interact with Varnish environment. Specifically it will directly rely on varnish agent instances in order to control varnish caches.

# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

  Pyvac runs on top of MongoDB and Flask, make sure you have mongo up and running with its default settings, 
  flask on the other hand will automatically be installed when running fab install.
  
* Version: 0.1
  
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

      sudo pip install fabric
      sudo fab install
  
  If the installation has been succesfull, open a terminal and type vac.
  
  This will enable you to use a full featured IPython shell against your Varnish-Agent installations. In order to make your Varnish-Agent visible
  to pyvac you need to restart the agent with the "-z" argument - asking for registration e.g. 
  
     "-z http://localhost:/8182/register". 
     
The address in the example is the default address where flask will run.
  
  Agent registration should be done only when the vac shell is running, as flask's lifetime is dictated by the shell's lifetime.
  
  The main class that provides agent management functionalities is called AgentTool and it is found under the vac.web.varnish.agent_tool _namespace.
  
  E.g.:
  
       at = vac.web.varnish.agent_tool.AgentTool() 
  
       at.list_nodes() - displays all registered agent instances.
  
       at.list_groups() - displays all custom created groups.
  
  Besides the methods exposed by the AgentTool in the shell, there is an extra set available for usage:

   * ping 
   * direct 
   * stats
   * vcljson
   * start
   * stop
   * paramjson
   * status
   * panic
   * echo
   * version
   * active_vcl
   * ban
   * log
   * package_string
   * help
   
  Any of the methods above accept as argument the name of the group upon which they will act. For instance:
  
      at.create_group('Staging')
      at.add_node_to_group('localhost:6085','Staging')
      at.ping('Staging') - will ping all the nodes that belong to the 'Staging' group.
  
  If any of these methods are called without an argument, then it is assumed that the method will act upon a single node which is set via the
  'set_current_node' command, e.g.:
  
     at.set_current_node('localhost:6085')
     at.ping()
     at.status()
  
* Configuration : Mongo runs on its default settings, no changes required here.
  Flask will start running on port 8182 when starting the shell, you can test that flask is up and running by issuing this in your browser: 
  [ Test Flask ](http://localhost:8182/test)
  
* Dependencies: All dependencies are fetched by **fab install**.
  
* Database configuration: None required.
  
* How to run tests: Run **fab test** in pyvac's root folder. It will run both unit tests and pep8.
  

### Contribution guidelines ###

* Writing tests: Add your tests under */vac/test/*

* Code review: Any code in pyvac should comply the pep8 standard. Run **fab test** to check your code.


### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact