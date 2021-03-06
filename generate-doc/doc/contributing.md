---
title: Contributing to Lugdunum
menu:
- title: Documentation
  href: /doc
  class: documentation button button-green align-right
---

# Contributing to Lugdunum

## Branching strategy

To have an efficient workflow, we chose to create different branches, each with their responsibility:
* `master`: the _master_ branch points to the latest stable release of the 3D engine. It is protected, which means that only trusted contributors can accept a pull-request to this branch. This branch guaranteed (up to a certain level) to be stable, and this is the only branch officially supported.
* `hotfix`: this branch is dedicated to critical bug fixes of the _master_ branch. Emergency fixes are committed to this branch directly, and a pull-request is opened to allow a quick code-review before pushing the changeset to _master_.
* `release`: this branch contains changes that one day will reside on _master_. They are present to allow users to test out new functionality before it is officially supported and bug-free.
* `dev`: this is the unstable, working branch. Changes on this branch may not be quite stable yet, and they might not work correctly on every platform. Once _dev_ is sufficiently stable, it is merged into _release_ (or cherry-picked).
* `feature-*`: these branches are feature branches, usually used by one or more developers working on a new feature. Only open pull-requests from these branches onto _dev_.

An example is shown in \autoref{fig:branching-strategy}, to demonstrate the utility of each branch, with a real-world scenario.
This branching strategy applies to all Lugdunum's projects and must be respected. As such, the branches `master` and `dev` are *protected* on Github, which means that only administrators have push access to these branches and that pull-requests with complete, passing tests must be opened to have changes implemented in these branches.

\pagebreak

<img src="./images/branching.pdf" style="width: 85%" alt="Branching strategy">

> [Brancing strategy]{#fig:branching-strategy}

# Testing architecture

Each commit pushed on each branch is compiled and tested by [CircleCI](https://circleci.com/gh/Lugdunum3D/Lugdunum) and [AppVeyor](https://ci.appveyor.com/project/Lugdunum/lugdunum).

You are encouraged to write tests for your code. A broken build is not be allowed in any case in a pull-request, be careful!


## Introduction

Unit tests cover all our sensible code. We use the [Google-Test](https://github.com/google/googletest/tree/master/googletest) framework which is considered as a third party module of our project. It is bound with [Google-Mock](https://github.com/google/googletest/tree/master/googlemock).

All the written tests can be found in the test folder of the [Lugdunum's repository](https://github.com/Lugdunum3D/Lugdunum/tree/dev/test    ) in the `dev` branch.

CMake and our CIs execute all the tests included in the folder `test`.  

## How to add new tests

If you want to add your tests, we recommend you to create a new folder in the `test` folder and put all your `*.cpp` in it. The structure of a test file should be like following : 

```cpp
#include <gtest/gtest.h>

TEST(myTestPool, myTest) {
    bool toto = true;
    EXPECT_EQ(toto, true);
}
```

To be compiled with other tests, each tests directory should have a CMakelists.txt. For example, in a `Math` directory, this file has the following format:

```md
# Tests directory path
set(SRC_ROOT ${PROJECT_SOURCE_DIR}/Math)

# Define *.cpp tests
set(SRC
    ${SRC_ROOT}/Geometry/Transform.cpp
    ${SRC_ROOT}/Matrix2x2.cpp
    ${SRC_ROOT}/Matrix3x3.cpp
    ${SRC_ROOT}/Matrix4x4.cpp
    ${SRC_ROOT}/Quaternion.cpp
)
source_group("src" FILES ${SRC})

# Add tests to compilation
lug_add_test(Math
             SOURCES ${SRC}
             DEPENDS lug-math
)
```

:::info
`source_group` on line 12 is a special CMake directive used for grouping source files in IDE project generation, for example, groups in Visual Studio. More information is available [on the official CMake documentation](https://cmake.org/cmake/help/v3.0/command/source_group.html).
:::

## Build tests

When using CMake, you need to add the command line argument `-DBUILD_TESTS`.
CMakes then creates one project for each test directory. In the previous example, it creates a `runMathUnitTests` project.
