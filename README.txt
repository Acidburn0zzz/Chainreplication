1) INSTRUCTIONS:
   There is a bash file called run in DistAlgoCode 
   Run the bash file and pass the config file path as the command line argument
   For example,
   ./run 'config/config1.json'
 
2) MAIN FILES: 
   DistAlgoCode has chainReplication.da which will read the config file and start the clients and the servers accordingly.
   DistAlgoCode/src/client/ has client.da which will spawn clients and handle message passing.
   DistAlgoCode/src/server/ has server.da which will spawn servers and handle message passing.
   DistAlgoCode/src/master/ has master.da which will spawn the master and handle message passing.

3) BUGS AND LIMITATIONS:
   -> Passing a non-existent config file or a config file which is not in the appropriate format will give an error.
   -> Cannot handle failures

4) CONTRIBUTIONS:
   We are a team of two (Praveen Alam and Kanchan Chandnani) and the project was divided in the following way:
   Kanchan coded the Client and the Master file in Erlang and DistAlgo, and made the configuration file for Erlang.
   Praveen coded the Server file in Erlang and DistAlgo, and made the configuration file for DistAlgo.
   The integration and debugging of the codes was a collabarative effort.
   

