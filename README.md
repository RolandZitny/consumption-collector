# Consumption Collector
This collector uses SLMP protocol through slmpclient library (https://pypi.org/project/slmpclient/) to obtain values
of energy consumption from 6 registers of Mitsubishi robotic arm. These values are generated approximately every 
3.5 millisecond and are all flushed in defined intervals (e.g. every 
 3 seconds). Both intervals are adjustable through environment attributes in 
***docker-compose.yml***. This file needs to be filled with all necessary information
like IP address of SLMP Server and so on.

### Classes
Consumption-collector consists of 2 classes:

* ***Communicator*** - communicates with SLMP server and saves all gathered data into *Collectors* internal queue. Every *communicator* has his own *collector* as attribute.
* ***Collector*** - collects data from *communicator* and flush them into InfluxDB in specific intervals.

### Preparation
Registers on Mitsubishi robotic arm  
