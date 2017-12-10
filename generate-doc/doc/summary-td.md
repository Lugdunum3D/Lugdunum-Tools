---
title: TD Summary
---

This document is intended for every potential Lugdunum contributor, or for everyone wanting to know a bit more about the internals of the project.

This document is split into two parts: the first focuses on Lugdunum, the 3D rendering engine, and on the other hand, the second is about LugBench, the benchmarking product.

In the first part of the document you will find an overview of the Lugdunum project, and details about how we interfaced with the Vulkan API. Each section is detailed with examples so that this document may be as simple and straightforward as possible, for developers of all levels.

It is however required that you have some background in 3D rendering and a working knowledge of your system (git, CMake, etc.) as we will not cover the basics, which are usually well documented on other documents and do not enter in the scope of this manual. When appropriate, useful links and resources are provided for your convenience.

The document ends with an information section, meant to answer the questions you could have after reading: for example how to report bugs, how to contact us, and other useful links.

In summary, when you finish reading this first part, you should have a rough idea of how Lugdunum's source code is designed, and you should be able to read through the files without any problems. If anything bugs you, please file an issue, and we will be glad to answer any question you may have.

The second part of the document presents the architecture of the API, front-end and desktop application of LugBench, the benchmarking software.