Instructions: 

1.	Open three separate terminals, and type the following lines in each one: 
a.	Python3 run.py 0
b.	Python3 run.py 1
c.	Python3 run.py 2
2.	When prompted, click enter to run the files 
3.	Open the log files folder to see the results (can be run as long as needed)
a.	[id] refers to the machine id number
b.	[speed] refers to number of operations able to be executed in a minute
c.	[logical clock time] – [system time] refers to the parameters specified in the investigation 
4.	Shut down the program when finished

Documentation: 

The code first initializes multiple virtual machines and will each have a logical clock at a clock rate determined randomly. For the clock ticks, it will pick a random number from 1 to 6 for each real world second and updates the logical clock accordingly. The initialization also involves connecting with other virtual machines, open files for the log, listen to other sockets, and have a network queue for the incoming messages. 

Our code will also start off with checking if there is a message in the queue. If there is none, then the machine will generate a random number from 1 to 10 where 1 sends a message to one of the machines with the local logical clock time, update its own, and update the log accordingly; if the number is 2, it sends to the other machine that is the local logical time, update its own clock and log, and if it’s three sends to both other machinese. If it’s none of the above, then there is no sending that takes place. If a machine then has the message in the queue, it will take one message off update the clock, and record down that it has received a message in the log. 

Finally, we will run the scale model at least five teams for at least one minute each and look at the different size of jumps in the logical clocks compared to the system time and how this is impacted by the different timings (by looking at message queues and logical clock gaps). The experimentation outline is mentioned below as well as the findings we have identified.  

Experimentation Scope:

Design Choices:

We have set the code up in a way where a given user can provide certain inputs that runs on different experiments (see the instructions side for what the parameters look like). We have utilized the creation of two sockets, one for receiving messages in one thread and the other for just sending.  By setting up this wire protocol and through a multi-threaded system, this ensures that there is no limbo zone where all the machines are waiting for a onnection without even starting the connection in the first place. Each new connection will also be started in a new thread and receive mssages there for the same reason. 







