# Analysis of DDoS Attacks in SDN Environments

## Course : Internet Technology and Applications 
## Course code : CO368

### Overview :
#### SDN :
Software-Defined Networking (SDN) is an emerging architecture that is dynamic, manageable, cost-effective, and adaptable, making it ideal for the high-bandwidth, dynamic nature of today’s applications. This architecture decouples the network control and forwarding functions enabling the network control to become directly programmable and the underlying infrastructure to be abstracted for applications and network services.<br>

<p align="center">
  <img width="480" height="526" src="https://qmonnet.github.io/whirl-offload/img/misc/sdn.svg"><br>
  <a align="center"> SDN Architecture </a>
</p>

#### DDoS :
A Denial-of-Service (DoS) attack is a cyber-attack where the attacker seeks to make a machine or network resource unavailable to its intended users by temporarily or indefinitely disrupting services of a host connected to the Internet. This is typically accomplished by flooding the target with superfluous requests in an attempt to overload systems.
In a Distributed Denial-of-Service (DDoS) attack, the incoming traffic flooding the victim originates from many different sources. This effectively makes it impossible to stop the attack simply by blocking a single source.
We have implemented two methods to detect DDoS attack in SDN environments
1. <b>Sample Entropy</b>
Sample Entropy is a method used to detect DDoS attacks in SDN. There are two essential 
components to DDoS detection using entropy: window size and a threshold. 
Window size is either based on a time period or number of packets. Entropy is calculated within 
this window to measure uncertainty in the coming packets. To detect an attack, a threshold is 
needed. If the calculated entropy passes a threshold or is below it, depending on the scheme, an 
attack is detected. 
2. <b>Prinicple Component Analysis</b> 
It is a mathematical procedure that transforms a number of 
(possibly) correlated variables into a (smaller) number of uncorrelated variables called principal 
components. The first principal component accounts for as much of the variability in the data as 
possible, and each succeeding component accounts for as much of the remaining variability as 
possible. 

### Steps to Reproduce :

Steps to reproduce along with the packages needed can be found [here](https://github.com/aswanthpp/Analysis-of-DDoS-Attacks-in-SDN-Environments/wiki/Steps-To-Reproduce) 

<<<<<<< HEAD
### Reference 

1. [A Novel DDoS Attacks Detection Scheme for SDN Environments](https://github.com/aswanthpp/Analysis-of-DDoS-Attacks-in-SDN-Environments/blob/master/reference/Base%20Paper.pdf)
2. 
3. 
 
=======
### Conclusion :

Results and conclusions along with output are included in [report](https://github.com/aswanthpp/Analysis-of-DDoS-Attacks-in-SDN-Environments/tree/master/reports) 


>>>>>>> a713301b97b4c3a550271ad46343e51420dc1e31
### Team : 
Aswanth P P (15CO112) <br>
Mohammed Ameen (15CO131) <br>
Joe Antony (15CO220) <br>
