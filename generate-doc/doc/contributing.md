# Contributing to Lugdunum

## Branching strategy

In order to have an efficient workflow, we chose to create different branches, each with its own responsability:
* `master`: the _master_ branch points to the latest stable release of the 3D engine. It is protected, which means that only trusted contributors can accept a pull-request to this branch. This branch guaranteed (up to a certain level) to be stable, and this is the only branch officially supported.
* `hotfix`: this branch is dedicated to urgent bug fixes of the _master_ branch. Emergency fixes will be commited to this branch directly, and a pull-request will be opened to allow a really quick code-review before pushing the changeset to _master_.
* `release`: this branch contains changes that one day will reside on _master_. They are present to allow users to test out new functionnality before it is officially supported and bug-free.
* `dev`: this is the unstable, working branch. Changes on this branch may not be quite stable yet, and they might not work correctly on every platform. Once _dev_ is sufficiantly stable, it will be merged onto _release_ (or cherry-picked).
* `feature-*`: these branches are feature branches, usually used by one or more developers working on a new feature. Pull-requests from these branch must be opened onto _dev_ only.

\pagebreak

Below is a quick schematic synthetizing all this information:

<img src="./images/branching.pdf" style="width: 100%">

## Tests

Each commit pushed on each branch is compiled and tested by [CircleCI](https://circleci.com/gh/Lugdunum3D/Lugdunum) and [AppVeyor](https://ci.appveyor.com/project/Lugdunum/lugdunum).

You are encouraged to write tests for your code. Broken build will not be allowed in any case in a pull-request, so be careful!
