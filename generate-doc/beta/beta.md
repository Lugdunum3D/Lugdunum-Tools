# Livrables

\begin{figure}[h]
\includegraphics[width=\textwidth]{./beta/schema_fonctionnel}
\caption{Schéma fonctionnel du projet (différents livrables avec les liaisons de communication entre eux), mettant en évidence les livrables concernés par la bêta.}
\end{figure}

\clearpage

## Scénario de Lugdunum

L'utilisateur de Lugdunum est un développeur expérimenté qui souhaite créer une application utilisant Vulkan à l'aide du moteur 3D Lugdunum.

Il télécharge donc les binaires de Lugdunum sur le site et crée une application à travers son API.

L'utilisateur installe les binaires, soit via les fichiers téléchargés précédemment ou via un packet (disponible sur Arch Linux via l'AUR).

Il peut ensuite créer son application en s'aidant de la documentation mise à disposition sur le site internet de Lugdunum.

L'utilisateur peut utiliser un système de "Log" pour afficher des messages sur les différents moyens d'affichage multi-plateformes (fichiers, sortie standard, LogCat d'Android, Visual Studio).


* Mise à disposition du moteur 3D
    * Un site web permettant de télécharger les sources et binaires : validé par le téléchargement des sources et des binaires sur le site
    * Un packet Arch-Linux contenant les binaires : validé par l'exécution de la commande suivante sur un système Arch Linux disposant de "pacaur" :
    ```
    pacaur -S lugdunum-engine
    ```
    On peut à présent vérifier la présence du moteur dans le système d'exploitation.
* Un build system utilisable par CMake (`FindLug`), démontré par le "live coding" d'une application "vide" qui compile avec Lugdunum.
    * L'utilisateur crée un dossier, vide, puis crée un projet C++ avec CMake, d'abord très basique (main "Hello World").
    * L'utilisateur ajoute la dépendence Lugdunum, et utilise un composant de lugdunum : include de fichier du Logger, puis utilisation du logger à la place de printf pour afficher "Hello, World"
* Un moteur 3D, validé par un "live-coding" démontrant l'utilisation de l'API du moteur, et validé par l'affichage de différentes scènes montrant différentes fonctionnalités:
    * Une première scène avec un modèle simple (e.g. un cube, sur un plan) et une lumière. Une interface ImGUI sera présente pour changer le type de la lumière pendant l'éxecution. Cela démontrera notre gestion des différents types de lumières et des ombres.
    * Une scène avec différents sphères ayant chacune un material PBR (*physical based rendering*). Chacun des materials de ces sphères auront différents paramètres (*roughness*, *metallic*, *texture*) montrant ainsi notre gestion des materials pbr.
    * Une scène affichant un modèle gltf.
    * Une scène avec de nombreux modèles et de nombreuses lights, d'abord chargée avec un renderer utilisant du Forward rendering, puis ensuite avec un renderer utilisant du Deferred rendering afin de montrer la différence de performance entre ces 2 techniques.
* Une documentation de la librairie Lugdunum
    * Validée par la navigation sur la documentation technique: https://lugdunum3d.github.io/docs/index.html
    * Validée par la navigation sur la documentation utilisateur depuis la page d'acceuil du site web: https://lugdunum3d.github.io/
    * Validée par l'ouverture de la version PDF des librairies 
* Le Logger : validé par la démonstration d'affichage de messages de log dans le programme précédemment développé.
* Le moteur est multi-plateforme (Windows, Android, Linux) : validé par l'affichage d'une scène sur différentes plateformes
* Une API mathématique permettant d'effectuer des transformations géométriques (translation, rotation, scaling)
    * Validée par l'exécution de la suite de test de cette dernière.
    * Validée par le live-coding d'une rotation dans un modèle simple, sur l'example "cube"
        * L'utilisateur part du sample cube qui a déjà la rotation mise en place
        * L'utilisateur démontre que le sample effectue une rotation
        * L'utilisateur commente les parties qui effectuent la rotation et qui utilisent la librarie mathématique, et démontre que la rotation s'arrête.

\clearpage

## Scénario de Lugbench

L'utilisateur de Lugdunum est une personne lambda qui souhaite tester les performances de son appareil (pc (Windows et Linux) et/ou appareil android) qui est compatible avec Vulkan.

Il télécharge donc l'application pré-compilée (exécutable) de LugBench sur le site et la lance. Cette dernière contient une interface permettant de lancer l'outil de benchmarking.

L'utilisateur lance le benchmarking, et plusieurs scènes lui sont proposées.
Il sélectionne une des scènes et cette dernière est affichée sur son écran.

L'outil de benchmarking va évaluer les performances de son appareil et les afficher, et va également les envoyer sur le serveur de LugBench, ainsi que certaines informations matérielles à des fins de catégorisation.

L'utilisateur peut accéder aux résultats des performances de tous les utilisateurs sur le site de LugBench.

* Mise à disposition de l'outil de benchmarking :
    * Un site web permettant de télécharger l'exécutable : validé par le téléchargement de ce dernier sur le site
    * Un packet Arch-Linux contenant les binaires : validé par l'exécution de la commande suivante sur un système Arch Linux disposant de "pacaur" : 
    ```
    pacaur -S lugbench
    ```
    On peut à présent vérifier la présence de LugBench dans le système d'exploitation.
* Un site web classifiant toutes les données des benchmarkings envoyées au serveur : validé par la navigation sur ce dernier
* Un outil de benmarking permettant d'évaluer les performances de son appareil sur différentes scènes: validé par le lancement de ce dernier
