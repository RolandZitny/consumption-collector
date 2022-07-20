# Consumption Collector
This collector uses SLMP protocol through slmpclient library (https://pypi.org/project/slmpclient/) to obtain values
of energy consumption from 6 registers of Mitsubishi robotic arm. These values are generated approximately every 
3.5 millisecond and are all flushed in defined intervals (every 
 3 seconds). Both intervals are adjustable.


- quary test ok ...
- msg 7/8/9/10/11 ms -> urzchlit
- -Batch/kod/c-language/??? 