## Ant Colony Simulation
### Ide
Simulera en myr koloni.  
#### Grundläggande principer
1. Myrorna lämnar stacken åt ett slumpmässigt håll.
2. Alla myror har en av fyra roller; *Seeker*, *Follower*, *Returner* eller *Returner2*
3. Om en myra hittar mat tar den med sig maten tillbaka till stacken.
5. En myra som bär mat lämnar ett feromon spår bakom sig.
6. Myror som letar efter mat följer feromon spåren för att öka sina chanser att hitta mat.  

När en myra hittat mat rör den sig så att dess distans hem alltid minskar men några slupmässiga svängar så den inte alltid går exakt raka vägen. Vid varje steg kollar alla *seeker* myror om det finns något spår i närheten, om så byter de till *follower* myror. Om en *follower* myra tappar spåret återgår den till en *seeker*.
### Funktion
``
Code stuff
``
### Referenser
* [Ants Simulation](https://itp.uni-frankfurt.de/~gros/StudentProjects/Applets_2014_AntsSimulation/ants.htm) av Peter Kuhn, Jannik Luboeinski, Laura Martin, Marius Schneider  
* [Ant Colony Simulations](https://softologyblog.wordpress.com/2020/03/21/ant-colony-simulations/) av Softology  
* [Ant Colony Simulation](https://www.rose-hulman.edu/class/cs/csse453/schedule/day40/AntColonySim.pdf) av Orion Martin, Josh Maurer, Tai Enrico, Sam Browder  
