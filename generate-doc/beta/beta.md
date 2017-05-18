---
title: Plan Bêta
---

# Livrables

<img src="./beta/schema_fonctionnel.pdf" width="100%"/>
> [Schéma fonctionnel du projet (différents livrables avec les liaisons de communication entre eux), mettant en évidence les livrables concernés par la bêta.]{#fig:schema-fonctionnel}


\clearpage

## Scénario de Communication

1. L'utilisateur ouvre le site vitrine et télécharge le framework Lugdunum pré-compilé pour sa machine.
    - Site vitrine
2. L'utilisateur visualise la documentation de Lugdunum en ligne, et sous format PDF.
    - Documentation Build Process
    - Documentation Technique
    - Documentation Utilisateur

## Scénario de Lugdunum

### Premier cas: Développeur de Lugnunum

L'utilisateur est un développeur souhaitant contribuer au développement du moteur 3D Lugdunum. L'utilisateur télécharge le moteur 3D Lugdunum depuis Github, via le site vitrine, avec git. Il crée un répertoire "code", puis clone le dépôt git dans ce repertoire. L'utilisateur peut à présent utiliser notre système de compilation utilisant CMake.

1. La compilation complète et réussie du moteur valide les fonctionnalités suivantes:
    - CMake Lugdunum
    - CMake find glTF2-loader
    - CMake glTF2-loader
    - Script d'automatisation pour les dépendences tierces

2. L'utilisateur, curieux de savoir si le projet est fonctionnel, peut à présent exécuter des tests unitaires afin de vérifier le fonctionnement de certaines parties du projet.
    - Librairie math (et toutes ses sous-fonctionnalités)
        - Vecteurs
        - Matrices
        - Quaternions
        - Fonctions géométriques
        - Tests unitaires
    - Gestionnaire d'allocation mémoire (et toutes ses sous-fonctionnalités)
        - Basic
        - Linear
        - Stack
 
3. Le développeur peut alors explorer les *samples* (examples) de notre projet. Ces examples sont des mini-programmes, voulus autonomes, qui dépendent de la bibliothèque Lugdunum. L'utilisateur va donc "installer" Lugdunum dans un répertoire de son choix, et ensuite indiquer aux systèmes de compilations des samples (CMake) ce dernier. Les samples utilisent une "macro" qui permet de trouver la bibliothèque Lugdunum dans ce chemin.
    - CMake Find Lugdunum
    - Classe d'abstraction d'application basique

4. Lors de son exploration, l'utilisateur va lancer deux exemples en particulier: L'exemple "base", qui va démontrer le fonctionnement du *Logger* (la journalisation) et des exceptions, ainsi que l'exemple "window" qui, comme son nom l'indique, va démontrer le fonctionnement des évenements clavier et souris.
    - Évenements claviers
    - Évenements souris
    - Fenêtres
    - Debug (assert, etc)
    - Journalisation des erreurs
    - Uniformisation des erreurs / exceptions

### Deuxième cas: Utilisateur du moteur 3D

L'utilisateur est un développeur souhaitant créer une application (par exemple, un jeu vidéo) utilisant Lugdunum comme moteur 3D. L'utilisateur télécharge une version pré-compilée de Lugdunum correspondant à sa plateforme. Il peut par ailleurs s'aider de la documentation mise à disposition sur le site internet de Lugdunum.

Lugdunum étant principalement une API de programmation, les parties ci-dessous se dérouleront en *live-coding*, c'est à dire que nous présenterons avec du code, des compilations et surtout des résultats les fonctionnalités du projet. C'est à dire que chaque étape ci-dessous résulte en un programme qui compile et qui présente le rendu décrit à l'écran.

5. L'utilisateur crée un nouveau projet en se basant sur le fonctionnement d'un *sample*. Dans cette nouvelle application, il souhaite afficher un cube, avec des vertices crées à la main, éclairé par une simple *Ambiant Light*. L'utilisateur crée donc ces objets, ainsi qu'une caméra basique. Ces deux objets (le cube et la lumières) seront ajoutés automatiquement au gestionnaire de resource et affichés grâce à la camera par le moteur. Cet énoncé, bien que court, implique le fonctionnement quasi-complet du moteur 3D, ansi que l'ensemble des abstraction de l'API Vukan. Sans celles-ci, il serait impossible que le cube s'affiche. Les fonctionnalités démontrées pour cette étape sont donc :
    - API bas niveau (et toutes ses sous-fonctionnalités)
    - Gestion des librairies partagés (chargement de Vulkan)
    - Forward rendering
    - Camera / synchronisation d'affichage
    - Génération dynamique de mesh
    - Lumière ambiante
    - Couleur d'un material / normale
    - Gestion centralisée des ressources

6. Le développeur souhaite faire tourner le cube. Il développe alors une solution utilisant des transformations afin d'éffectuer cette rotation, le tout controllé par la gestion du temps fournie par la bibliothèque Lugdunum. 
    - Transformation (Gestion de scène)
    - Gestion de timer

7. Démonstration des Viewports paramètrables par l'ajout d'une deuxième vue qui prend la moitié de l'écran, et qui affiche le cube sous un autre angle, à l'aide d'une seconde caméra. Cette étape démontre donc :
    - Customs Viewports

8. Implémentation d'une caméra en vue libre car l'utilisateur souhaite pouvoir se déplacer autour du cube avec les touches de son clavier. Pour pimenter les choses, l'utilisateur attache une *Spot Light* sur une des deux caméras. Également, l'utilisateur développe de manière rapide une GUI permettant de changer la couleur de la lumière attachée à la caméra.
    - Camera libre
    - Lumière spot
    - GUI

9. Remplacement de la *Spot Light* par une *Point Light* et de l'*Ambiant Light* par une *Directional Light*.
    - Lumière point
    - Lumière directionnelle

10. L'utilisateur développe une nouvelle scène contenant plusieurs sphères, chacune ayant un dégradé sur leur matériau des paramètres *metallic* et *roughness*. Comme on utilise des matériaux, le rendu validera la fonctionnalité "Rendu PBR". Certaines fonctionnalités de l'ancienne scène, telle que la Caméra Libre, les lumières etc. seront reprises dans cette démonstration. Cette étape démontre alors :
    - PBR
    - Metallic
    - Roughness

11. L'utilisateur crée un nouvel exemple contenant maintenant plusieurs sphères, côte à côte, présentées, compilées et démontrées successivement, démontrant à chaque fois l'ajout de paramètres du materiau des sphères. Autrement dit, chaque sphère reprendra les paramètres de la sphère située à côté d'elle, en ajoutant un nouveau pramètre. Les paramètres démontrées sont donc les suivants :
    - Chargement des textures
    - Diffuse texture
    - Metallic Roughness Mapping
    - Normal map
    - Ambient occlusion map
    - Emissive
    - Emissive map

12. Maintenant que nous avons démontré que l'utilisateur peut utiliser des fonctionnalités "bas niveau" du moteur, c'est-à-dire sans gestion avancée de scènes, tous les objets étaient créés "à la main", nous pouvons nous atteler au chargement d'une scène depuis un fichier glTF 2.0. Cette scene contient quatre cubes, chacun avec une texture d'un format différent (jpg, png, tga, bmp). Les fonctionnalités démontrées par cette étapes sont les suivantes :
    - Gestion des modèles GLTF 2.0
    - glTF2-loader
        - Chargement de modèles au format json
        - Chargement de textures
            - PNG
            - JPG
            - TGA
            - BMP
13. Dernière étape de démonstration du moteur 3D: Chargement d'une scène complète depuis un fichier glTF 2.0 et création d'une *Skybox* (ciel). L'utilisateur crée un programme qui charge le modèle ainsi que le ciel, compile et lance le programme.
    - Gestion des modèles GLTF 2.0
    - Skybox

\clearpage

## Scenario de LugBench

1. L'utilisateur se connecte sur le site web de LugBench. Il peut consulter les résultats déjà soumis par d'autres utilisateurs. L'utilisateur peut également récupèrer l'éxecutable pour sa plateforme sur site web, afin d'éxectuer lui-même le test, et de téléverser ses données sur le site.
    - Site web de presentation des données

2. L'utilisateur lance l'application et un menu lui permettant de lancer le test de benchmarking s'affiche. Lors du clic sur le bouton, l'utilisateur peut visualiser la scène en train d'être affichée, il ne peut néanmoins pas intéragir avec, cette scène servant à tester son matériel, il faut que le rendu soit le même, peu importe l'utilisateur et peut importe le périphérique. Une fois le test finit, l'application revient sur le menu principal.
    - GUI de l'application
    - Exécution des scènes
    - Récupération des spécifications Vulkan
    - Envoie des specs utilisateur au serveur
3. L'utilisateur retourner ensuite sur le site internet afin de visualiser ses résultats, ainsi que ceux des autres utilisateurs.
    - RestAPI
    - Base de donnée (MongoDB)
    - Affichage sous forme de tableau
    - Génération de score
4. Enfin, le logiciel LugBench est compilé sur plusieurs services d'intégration continue, notemment CircleCI et AppVeyor. Lors de ces compilations, le système de compilation CMake est utilisé, ainsi que le système de téléchargement des dépendences tierces. La vérification de *builds* réussis sur ces plateformes démontrent les fonctionnalités suivantes :
    - CMake
    - Third party integration
    - Script d'automatisation
