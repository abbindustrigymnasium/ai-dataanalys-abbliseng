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

---
### Ants
#### Seeker
Myrorna letar åt en av 8 riktningar (illustrerat i bilden nedan). Beroende på vilken av de tre möjliga de väljer så kan de byta riktning genom att svänga. Om t.ex. en ruta som nedan märkts med -1 väljs innebär detta att myran kommer minska sin riktning med 1 och därmed röra sig motsols i diagrammet nedan. Om den har riktning 6 kommer den alltså nästa gång ha riktning 5.
![Myrornas olika riktningar](https://github.com/abbindustrigymnasium/ai-dataanalys-abbliseng/blob/master/AI%20projekt/AntColonySimulations/Resources/AntDirections.PNG)
#### Follower
*Follower* myrorna följer efter pheromon spår som tidigare myror lämnat bakom sig när de gått hem med mat. De samlar information om alla 8 områngande rutor och utifrån de nedstående parametrarna rankar dessa.
* PH koncentration
* Distans från myrstacken
![Kod Exempel 1](https://github.com/abbindustrigymnasium/ai-dataanalys-abbliseng/blob/master/AI%20projekt/AntColonySimulations/Resources/Kod1.PNG)
Utifrån detta beräknas sedan ett värde eller *vikt* för rutan och sedan väljs vilken ruta med större sannolikhet desto bättre.
![Kod Exempel 2](https://github.com/abbindustrigymnasium/ai-dataanalys-abbliseng/blob/master/AI%20projekt/AntColonySimulations/Resources/Kod2.PNG)
#### Returner
Det finns två olika *returner* myror.
##### De som lämnar spår bakom sig
Dessa är de myror som hittat mat och som går hemmåt och lämnar därmed feromoner bakom sig. De går mer eller mindre raka vägen hem med några slumpmässiga svängar.
##### De som inte gör det
En myra blir en klass 2 returner om den antingen nått sin max distans eller nuddar en vägg. Dessa går på samma sätt som de första returners men dessa lämnar inga feromon spår bakom sig.

---
### Map
"Spelbrädet" är uppbyggt av *MapPoints*. Det finns en *MapPoint* per pixel på skärmen och dessa håller följande information:
* Typ
* Decay Constant
* Position
* Display objekt
* Feromon nivå
*MapPoint* klassen innehåller också funktionerna relaterade till att rita ut pixeln och hantera feromonerna.
#### Typer
Det finns precis som med myrorna flera olika typer av *MapPoints*; *Nest*, *Food*, *Empty*, *Obstacle*.
Dessa har lite olika funktioner med det är rätt självförklarande. *Nest* är själva myrstacken där myrorna börjar och t.ex. lämnar maten. *Food* är mat punkter, om en myra hittar en blir den en *returner* av typ 1 och *MapPoint*en klassas om till en av typ *empty*. *Obstacle*s är bara *MapPoints* myror inte kan befinan sig på/gå igenom.

---
### Referenser
* [Ants Simulation](https://itp.uni-frankfurt.de/~gros/StudentProjects/Applets_2014_AntsSimulation/ants.htm) av Peter Kuhn, Jannik Luboeinski, Laura Martin, Marius Schneider  
* [Ant Colony Simulations](https://softologyblog.wordpress.com/2020/03/21/ant-colony-simulations/) av Softology  
* [Ant Colony Simulation](https://www.rose-hulman.edu/class/cs/csse453/schedule/day40/AntColonySim.pdf) av Orion Martin, Josh Maurer, Tai Enrico, Sam Browder  
