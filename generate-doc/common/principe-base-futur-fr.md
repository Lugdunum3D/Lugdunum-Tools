---
title: Principe de base du système futur
---

## Principe de base du système futur

### Présentation de la technologie Vulkan

Vulkan est une nouvelle génération d’interface de programmation (API^[API : Ensemble normalisé de classes, de méthodes, ou bien de structures de données par lequel un logiciel offre des services d’utilisation ou de communication.]) permettant un rendu 3D optimisé et multiplateforme. C’est une nouvelle technologie crée par le Khronos Group, un consortium se focalisant sur le développement de standards libres.

Nos ordinateurs et nos téléphones sont tous équipés aujourd’hui de puces graphiques spécialisées dans le calcul de scènes 3D complexes. Afin d’en tirer avantage, nous devons donc communiquer avec celle-ci, par l’intermédiaire d’une API: Vulkan dans notre cas.

Pouvoir communiquer avec la carte graphique afin d’effectuer le rendu d’une scène 3D n’est pas un principe nouveau. Il existe depuis des années deux API massivement utilisées sur le marché actuel : DirectX, exploitable uniquement depuis le système d’exploitation Microsoft Windows et OpenGL qui est libre et fonctionne de façon multiplateforme.

DirectX et OpenGL sont des technologies qui ont été respectivement annoncées en 1995 et 1997, et qui malheureusement reflètent toujours aujourd’hui les architectures matérielles et logicielles de l’époque. Par exemples, elles ne permettent pas de profiter et d’exploiter les architectures multi-cœurs modernes des ordinateurs et téléphones d’aujourd’hui. Nous pouvons cependant remarquer que Microsoft a fait un réel effort avec sa dernière version de DirectX (DirectX12, annoncé en 2015), et a mis à jour en profondeur son API afin qu’elle puisse être mieux adaptée aux appareils récents. Étant une technologie propriétaire de Microsoft, DirectX12 n’est malheureusement compatible que sur les appareils équipés du dernier système d’exploitation du groupe, Windows 10.

Ces APIs historiques présentent également d’autres problèmes : il faut savoir que la carte graphique ne peut comprendre qu’un langage très complexe. Pour rendre leur utilisation plus aisée, DirectX (versions 11 et antérieures) et OpenGL proposent une couche de transition de ce langage complexe avec un langage plus simple à comprendre pour le développeur. Ce langage est donc "traduit" par l’interface de programmation avant d’être retransmit à la carte graphique. Ce processus d’interprétation, en plus d’être approximatif, reste fâcheusement très dépendant du système sur lequel il est effectué. Cette façon de faire résulte donc en des performances nonuniforme suivant la plateforme où le rendu 3D est effectué (ordinateur de bureau, tablette, téléphone, console).

Comme DirectX 12, Vulkan résout ces problèmes en étant une interface de programmation moderne, exploitant correctement les ressources des appareils d’aujourd’hui. Avec Vulkan, l’ordre transmis par le programmeur à la carte graphique est beaucoup plus complexe. Le processus de transformation est par conséquent réduit au maximum réglant le problème de performance inégales d’OpenGL / DirectX. Cela rend cependant l’utilisation de Vulkan assez complexe et donc exclusive aux programmeurs expérimentés.

### Les inconvénients de Vulkan

Vulkan étant une technologie extrêmement récente, les entreprises du secteur ne peuvent pas encore se permettre de miser sur cette dernière, car elle n’a pas encore fait ses preuves dans le milieu professionnels.

Le fonctionnement radicalement différent de Vulkan comparé aux APIs historiques obligerait aussi aux entreprises d’investir de l’argent et un temps considérable pour former leurs employés à la nouvelle technologie. Vulkan n’étant pas retro-compatible avec les anciennes APIs, les programmes existant doivent être en grande partie restructurés afin de les rendre non seulement compatibles, mais aussi présentant des performances égales voire supérieures que les anciennes APIs. Aujourd’hui, seules certains géants comme Google, NVIDIA et AMD peuvent se permettre d’y investir des équipes spécialisées.

Pour finir, le plus gros point noir de Vulkan est le nombre d’appareils compatibles. Toutefois, étant un standard libre proposé par Khronos Group, le consortium réunissant les géants du secteur, la grande majorité des appareils sortant à partir de fin 2016 sont compatibles Vulkan. Malgré cela, étant donné la part de marché actuelle des appareils supportant Vulkan, il serait risqué pour une entreprise de miser exclusivement sur cette nouvelle technologie. C’est justement pour cette raison qu’un groupe d’étudiants tel que le nôtre se trouve en bonne position pour effectuer cette démarche de R&D au sein de notre projet de fin d’études.

### Notre projet

Notre projet se compose en deux axes majeurs:

* D'un coté, le developpement d'un moteur 3D qui est construit autour d'une nouvelle technologie, Vulkan. Cette technologie permet l'affichage en temps réel de scènes 3D de manière optimisée sur un ensemble de plateforme allant de l'ordinateur de bureau classique jusqu'aux plateformes mobiles telles que les smartphones et les tablettes. Le moteur a également la particuliarité de gerer un modèle d'illumination qui respecte les lois de la physique afin d'obtenir un rendu photoréaliste. 

* Enfin, afin de démontrer la pertinance de notre moteur 3D, nous developpons également un logiciel qui exploite la technologie de celui-ci. Ce logiciel est un outil permettant de mesurer les performances d'une puce graphique d'un smartphone ou d'un PC en mesurant sa performance lors de l'affichage fluide de scènes 3D complexes.

<img src="http://svgshare.com/i/1bw.svg" width="100%">
>[Diagramme présentant les acteurs intéragissant avec notre projet et ses différents composants]{#fig:principe-logigramme}