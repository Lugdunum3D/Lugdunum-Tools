---
title: Cahier des charges
---


# Description des différentes parties du programme à réaliser

## Lugdunum

<img src="http://svgshare.com/i/1fp.svg" width="60%"/>

> [Logigramme des six composants de Lugdunum]{#fig:lugdunum-components}

Lugdunum s'architecture en six composants ayant chacun un rôle bien défini :
- **Core** sert de base à toutes applications souhaitant utiliser notre API.
- **System** s'occupe de la gestion de la mémoire, du temps (timer/clock), des exceptions, du logger et du chargement des bibiliothèques dynamiques.
- **Maths** fournit tous les outils mathématiques nécessaire à notre API graphique. Elle permet l'utilisation des matrices, vecteurs, quaternions ainsi que d'autres outils travaillant sur ces objets tel que les matrices de transformation et la trogonométrie.
- **Graphics** est la partie principale du framwework; elle contient l'essentiel du moteur 3D : l'abstraction de Vulkan, la gestion des ombres, des lumières, etc.
- **Window** permet d'avoir accès à une fenêtre d'affichage du rendu 3D sur tous les systèmes d'exploitation supportés.
- **glTF2-loader** est une bibliothèque, presque "externe" au projet, disponible de manière indépendante et autonome. Elle permet le chargement de modèles 3D au format glTF2.0, qui est très récent et assez porté par la communauté intéressée à la technologie Vulkan. En effet, glTF est un format édité par le même consortium qui édite Vulkan, Khronos Group.


Ces composants ont tous des points communs :
- Gestion des erreurs et du logging (implémentés dans la bibliothèque *System*)
- Noms de fonctions cohérentes et logiques entre les différentes parties
- Documentation complète et élaborée
- Style du code cohérent, élégant et imposé aux contributeurs

### Le moteur 3D

Le moteur 3D est le cœur de notre projet. Il est disponible sous la forme d'une bibliothèque, compatible avec les matériels disposant d'une carte graphique supportant l'API Vulkan. Il comprend le composant *Graphics* énoncé auparavant, et utilise la bibliothèque *glTF2-loader* afin de charger des modèles 3D.
Elle implémentera les fonctionnalités suivantes :
- Système de caméra virtuelle, soit fixe, soit en caméra libre (type FPS)
- Gestion de modèles au format glTF2.0, textures aux formats PNG, JPG, TGA et BMP
- Instancing
- Lumières (*Point Light* / *Directional Light* / *Spotlight* / *Ambiant Light* / *Diffuse*), ombres, bloom
- Antialiasing
- Interface graphique 2D (GUI) utilisant [imgui](https://github.com/ocornut/imgui)
- Optimisations (*Deferred shading*, *Deferred lighting*, *Tesselation*,         *Pipeline cache*)

### Bibliothèque *System*

La bibliothèque système fournit des fonctionnalités diverses et multiplateformes permettant d'harmoniser le fonctionnement de l'ensemble du projet, par exemple en implémentant des mécanismes de gestion d'erreurs, ainsi que des fonctionnalités supplémentaires à la librairie standard du C++ :
- Journalisation (*Logging*)
- Gestion d'erreurs et exceptions
- Chargement de biblothèques dynamiques externes pendant l'éxecution
- Gestion optimisé des allocations de mémoire
- Thread pool
- Read / Write mutex (primitives de synchronisation)
- Gestion du temps

### Bilbiothèque *Window*

Vient ensuite le composant *Window* (fenêtre) qui, comme son nom l'indique, gère l'ouverture de la fenêtre et la surface d'affichage des rendus 3D. Elle gère également les évenements tels que la fermeture et redimentionnements de la fenêtre, mais aussi les pressions de touches de claviers, mouvements et pressions de boutons de la souris et les actions de l'écran tactile sur la plateforme Android. Ces différents évenements, bien-sûr spécifiques à chaque plateforme (Linux, Android et Windows) sont abstraits afin que l'utilisateur final n'ait à gérer que la version de Lugdunum.

### Bibliothèque *Math*

La bibliothèque math permet de gérer des concepts mathématiques plus "haut niveau" que les opérations mathématiques de base supportées par la librairie standard. Elle est utilisée pour les calculs 3D du moteur.
- Vecteurs
- Matrices
- Quaternions
- Frustum

### Autres

Comme ce projet est open source (disponible sur la plateforme GitHub), nous avons également à disposition des utilisateurs différentes plateformes :

#### Site vitrine
Le site web sert principalement de plateforme de téléchargement du moteur 3D et de ses différentes bibliothèqyes. Il permet de retrouver à un seul endroit les liens vers :
- Le code source
- La documentation
- Le téléchargement des différentes releases

#### Documentation, guides de démarrage rapide et de prise en main

La documentation est une étape très importante dans un projet open source. Un projet mal documenté est un échec assuré. Elle est le point d'entrée des nouveaux utilisateurs qui vont pouvoir découvrir les possibilités offertes par notre solution et elle sera consultée constamment par les personnes qui utiliseront Lugdunum.

Toute la documentation du projet est visible sur notre site internet ainsi que sur notre dépôt GitHub. La documentation consiste d'une part à une référence de l'API générée à l'aide de l'outil [Doxygen](http://www.doxygen.org/) et d'autre part une documentation utilisateur qui est constiuée de différents guides et tutoriels introduisant nos utilisateurs à nos solutions.

#### Bug tracker

Cette plateforme permet aux utilisateurs qui rencontrent des problèmes lors de l'utilisation du moteur 3D ou qui ont des questions et des suggestions de nous faire part de ces élements.
Ces tickets sont visibles de manière publique au sein de notre [dépôt GitHub](https://github.com/Lugdunum3D/Lugdunum/issues); un système reconnu et acclamé par les développeurs dans le monde entier.

## LugBench

LugBench est un ensemble d'outils permettant d'évaluer les performances d'une puce graphique en executant une scène 3D complexe et de les rendre publiques sur notre site web à des fins de catégorisation.

<img src="http://svgshare.com/i/1bR.svg" width="40%"/>

>[Logigramme des trois composants de LugBench]{#fig:lugbench-components}

### Application

L'application est lancée par l'utilisateur sur sa machine. Elle permet d'exécuter des scènes de rendu 3D. Suivant les performances du système, l'applicaion attribuera à celui-ci un score.
L'application récupere également les différentes informations matériel du système et envoie ces informations au server par l'intermédiaire de l'API.

### L'API

LugBench-API est un server web permettant recevoir, de stocker et de formatter les informations qu'envoie l'application.

### Website
Le site web affiche, sous forme de tableau comparatif, l'ensemble des résultats de la base de données de l'API afin de comparer les performances des différents systèmes.


# Présentation de l'environnement de réalisation

## Environnement de réalisation

Les deux projets Lugdunum et Lugbench respectent le même environement de réalisation ainsi que les mêmes contraintes.

Ce projet comportant une grande quantité de code source complexe, celui-ci se doit d'être normé et encadré afin de maintenir un certain standard de qualité. Pour cela nous imposons un guide de style de programmation, ou *guideline* afin d'uniformiser le code source et d'établir des bonnes pratiques. Le fait d'imposer une *guideline* permet de ne pas imposer forcément un IDE, tous les membres de l'équipe sont libres d'utiliser l'IDE qu'ils souhaitent du moment qu'ils respectent les normes mises en place.
Pour le versionning du code source, nous utilisons le logiciel git, couplé avec la plateforme GitHub, qui est de loin le couple le plus utilisé dans le monde de l'Open-Source.
En effet, cette plateforme comprend de nombreuses fonctionnalités qui permettent de simplifier la visualisation et l'avancement d'un projet. Nous avons notamment accès directement au code source en ligne et a des fonctionnalités permettant de réaliser le projet dans de bonnes conditions, comme la revue de code obligatoire. Le système d'*issues* nous permet de remonter des bugs au fur et à mesure du développement et le système de PR (*pull request*) nous permet de travailler de manière collaborative et organisée (voir \autoref{organisation-projet}). Ces deux systèmes permettent d'assigner des personnes, des *deadlines* et de discuter publiquement, et nous permettent de rester organisé dans la gestion des problèmes et l'incorporation de nouvelles fonctionnalités.
Sur un projet avec autant de contributeurs (notre équipe étant nombreuse), il faut que le *versionning* du projet soit normé et strict. La \autoref{fig:branching-strategy} montre notre stratégie de *branching*, les merges de fonctionnalités et des hotfixes ne se font que par PR. Le reste des merges se fait par une seule et unique personne pour assurer l'intégrité de cette tâche.
Les tests se font en deux étapes, les tests unitaires et les tests d'intégrations. Les tests unitaires sont testés à chaque *push* sur le dépôt Github via APIs permettant de connecter des services de tests unitaires distants. Nous utilisons [CircleCI](https://circleci.com/gh/Lugdunum3D/Lugdunum) et [AppVeyor](https://ci.appveyor.com/project/Lugdunum/lugdunum/). Ces outils permet en effet d'avoir une compilation exécutée en parallèle de manière automatique et gratuite, de façon extrêmement simplifié. GitHub nous informe ensuite si la fonctionnalité développée passe bien les tests. Ces tests unitaires sont développés au fur et à mesure de l'ajout de fonctionnalités.
Les tests d'intégrations permettent de tester de véritables samples et démos sur les différentes plateformes. Ceci doit être fait manuellement car il est difficile de mettre en place une plateforme de tests d'intégration pour des rendus 3D. Ils permettent de s'assurer du côté multi-plateforme du projet de manière régulière, en effet si un bug apparait lors de ces tests, une issue est créée par la personne ayant effectué le test.

Le moteur 3D Lugdunum et la partie application de bureau de LugBench utilisent tous les deux l'outil de compilation CMake, afin de respecter la contrainte d'être compatible avec les plateformes Linux, Windows et Android. En effet, utiliser CMake pour construire notre système de compilation nous permet de créer une seule configuration qui peut être utilisée pour générer des fichiers "projets", tels que des solutions Visual Studio, Android Studio ou des simples Makefiles.

<img src="./images/branching-fr.pdf" style="width: 85%" alt="Branching strategy">
> [Stratégie de _branching_]{#fig:branching-strategy}

Pour la partie web de LugBench plus spécialement, certains aspects sont différents:
- L'API : Cette partie utilise [Express](http://expressjs.com). Express permet de concevoir une infrastructure web minimaliste, souple et rapide pour [Node.js](https://nodejs.org). Cette partie nécéssite également une basse de données. Pour celle-ci, nous avons choisi [MongoDB](https://www.mongodb.com). MongoDB est une base de données NoSQL rapide et permettant un stockage important de données. La gestion du projet et des dépendances se fait directement avec [NPM](https://www.npmjs.com), un outil associé à NodeJS. La *guideline* énoncée plus haut n'est pas utilisée dans ce sous-projet, en raison du langage différent (JavaScript).
- Le site web: Cette partie utilise principalement [Angular2](https://angular.io). Angular2 est une référence dans le monde du web front-end. Il est rapide, permet d'avoir une organisation de projet efficace et possède une grande communauté. Nous utilisons Angular2 avec [TypeScript](https://www.typescriptlang.org). TypeScript nous permet un typage des variables. Ainsi, il rend le code plus portable et plus compréhensible pour les développeurs. Nous utilisons [Bootstrap](http://getbootstrap.com) pour la gestion de l'affichage du site sur différents terminaux de nos utilisateurs. Grâce à [Gulp](http://gulpjs.com) et [NPM](https://www.npmjs.com), on peut facilement gérer la génération et les dépendances du projet.

## Composants existants

### Lugdunum

L'ensemble des dépendences du projet Lugdunum, pour sa partie moteur 3D, sont open-source. Elles sont douc disponibles de manière intemporelle et maintenues à la volonté libre de la communauté et/ou des entreprises à l'origine de ces projets. Nous avons choisi avec soin nos dépendences selon des critères tels que le nombre de "stars" sur leur page GitHub, un bon indicateur de popularité, qui permet en quelque sorte de nous assurer que le projet est utilisé par un grand nombre d'autre projets, et donc qu'il a plus de chances d'être maintenu dans les années à venir.

- [Vulkan](https://en.wikipedia.org/wiki/Vulkan_(API)) est l'api graphique bas niveau que nous utilisons.
- [glTF2.0](https://github.com/KhronosGroup/glTF/tree/2.0/specification/2.0) est la version 2.0 de la spécification glTF, qui est un format libre et ouvert de modèles 3D compatibles PBR^[PBR: Physically Based Rendering: \url{https://en.wikipedia.org/wiki/Physically_based_rendering}].
- [imgui](https://github.com/ocornut/imgui) est une bibliothèque C++ légère permettant d'afficher une interface graphique basique.
- [fmt](https://github.com/fmtlib/fmt) est une bibliothèque de formattage de chaînes de charactères, utilisée dans nos outils de journalisation.
- [stb_image](https://github.com/nothings/stb/blob/master/stb_image.h) est une bibliothèque qui se constitue que d'un seul fichier et qui permet de charger des images aux formats PNG, JPG, TGA et BMP, entre autres.
- [googletest/googlemock](https://github.com/google/googletest) est le framework qui nous sert à réaliser l'ensemble de nos tests unitaires.

### LugBench

Comme Lugdunum, toutes les dépendances du projet LugBench sont open-sources. Elles seront donc disponibles tant que la communauté open-source maintient ces projets.

##### Composants existants pour l'API

- [Express](http://expressjs.com) permet de concevoir une infrastructure web minimaliste, souple et rapide.
- [Node.js](https://nodejs.org) permet de concevoir un serveur web fiable et performant en JavaScript.
- [NPM](https://www.npmjs.com) permet de gérer efficacment un projet et ses dépendances.
- [MongoDB](https://www.mongodb.com) est une base de donnée NoSQL performante.

##### Composants existants pour le site web

- [Angular2](https://angular.io) permet de concevoir des interfaces web rapides et fiables.
- [TypeScript](https://www.typescriptlang.org) permet le typage des variables JavaScript.
- [NPM](https://www.npmjs.com) permet de gérer efficacment un projet et ses dépendances.
- [Gulp](http://gulpjs.com) permet l'éxecution de tâches, la génération du projet par exemple.

##### Composants existants pour l'application de bureau

- [libcurl](https://curl.haxx.se/libcurl/) est _la_ bilbiothèque standard pour effectuer des requêtes HTTP dans un code C/C++.
- [restclient-cpp](https://github.com/mrtazz/restclient-cpp) est une enveloppe autour de libcurl nous permettant d'utiliser les fonctionnalités modernes de C++ avec comme _backend_ libcurl.
- [json](https://github.com/nlohmann/json) permet de sérialiser des éléments dans un code C++ en une syntaxe JSON, afin de les envoyer sur le réseau internet.

## Gestion de la sécurité

### LugBench

Pour l'API de LugBench, la sécurité est importante. Le bon fonctionnement de l'API et du site web en dépendend directement.  Nous avons mis en place une validation des requêtes avec [Joi](https://github.com/hapijs/joi). Ainsi, l'utilisateur ne peux pas insérer un objet défectueux en base. Nous avons aussi mis en place une limitation du nombre de requêtes par utilisateur. Cette limitation permet de limiter les effets d'un utilisateur malveillant.

Pour le site web, une simple validation des champs en HTML5 est mise en place.


## Points sensibles

### Lugdunum

Notre projet vise l'ensemble des plateformes desktop et mobiles compatible Vulkan. Il y a donc le risque qu'une nouvelle plateforme que nous comptons supporter apparaisse sur le marché et que nous devions la supporter. C'est par exemple possiblement le cas de Apple qui pour le moment n'a pas déclaré vouloir supporter Vulkan sur macOS et iOS mais pourrait peut-être le supporter d'ici quelques mois ou années.
Notre politique dans ce cas-ci n'est pas de supporter ces plateformes, mais de faire en sorte que ces plateformes puissent être supportées sans trop de changements.

### Lugbench

Le point sensible de Lugbench est la sécurisation de l'API. Malgré la validation des requêtes et la limitation de requêtes par minute, si un utilisateur malveillant arrive à corrompre la base ou à remplir la base avec des données non pertinentes, l'application Lugbench peut subir des interruptions de service. Nous allons mettre en place un système de sauvegarde de la base de données pour prévenir ce genre de problème, afin d'être capable de restaurer une version des données saine dès lors que l'on détecte un acte de sabotage.

# Organisation projet

Pour être rigoureux dans la réalisation de ce projet nous devons savoir qui fait quoi et quand. Chaque fonctionnalité de notre projet fait l’office d’une tâche qui sera réalisée par une ou plusieurs personnes ce qui donnera suite à une PR.

Pour savoir qui va suivre l’avancement du travail d’une tâche (pour être sûr qu’elle avance sans problèmes) et valider la PR de celle-ci, un responsable sera nommé pour chaque « catégories » de fonctionnalités.

Par exemple s’il y a un responsable X sur le moteur de rendu 3D, un responsable Y sur le scène manager et que la personne Z réalise une tâche lié au scène manager, la PR pour cette tâche sera créé par Z, et sera validé par X et Y. Si Z ne réalise pas son travail, ou à des problèmes pour avancer, les deux responsables X et Y seront là pour épauler Z.

Les personnes ayant accès à une plateforme en particulier (par exemple Antoine qui a un téléphone Android compatible Vulkan), seront responsable de réaliser les tests d’intégrations de cette dernière de manière régulière. En cas de problème, une issue sur Github est crée avec le descriptif du problème et le responsable de la partie y est assigné.

En effet, un bug sur la gestion des ombres sera géré et corrigé par le développeur responsable de cette fonctionnalité, si le problème n’apparait que sur une seule plateforme, sa résolution se fera en collaboration avec la personne qui a effectué le test d’intégration.

4 à 6 membres travaillent à plein temps sur Lugdunum, deux membres du groupe sont à plein temps sur la partie LugBench. D'autres membres peuvent venir les aider sur des tâches difficiles ou chronophages.
