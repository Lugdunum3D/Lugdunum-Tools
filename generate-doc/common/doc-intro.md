# Introduction

## Why Vulkan?

Vulkan is a new generation of APIs for optimized, cross-platform 3D rendering. It is a new technology created by the Khronos Group, a consortium focused on the development of free standards.

Our computers and phones are all equipped with graphics chips that specialize in calculating complex 3D scenes. In order to take advantage of it, we must communicate with it, through an API: Vulkan in our case.

Being able to communicate with the graphics card in order to render a 3D scene is not a new principle. For years, there have been two widely used APIs on the market today: DirectX, which can only be run on the Microsoft Windows operating system and OpenGL, which is free and operates on a multi-platform basis.

DirectX and OpenGL are technologies that were announced in 1995 and 1997 respectively, and unfortunately still mirror the hardware and software architectures of the time. For example, they do not make it possible to take advantage of and exploit the modern multi-core architectures of today's computers and phones. However, we can point out that Microsoft has made a real effort with its latest version of DirectX (DirectX12, announced in 2015), and has updated its API in depth so that it can be better adapted to recent devices. Being a Microsoft proprietary technology, DirectX12 is unfortunately only compatible with devices equipped with the group's latest operating system, Windows 10.

These historical APIs also present other issues: graphics card can only understand a very complex language, and to make them easier to use, DirectX (versions 11 and earlier) and OpenGL offer a transition layer of this complex language with a simpler language to use for the developer. It is then "translated" by the API before being relayed to the graphics card. This process of interpretation, in addition to being quite approximate, is very much dependent on the system on which it is performed. This way of doing so results in nonuniform performances depending on the platform where the 3D rendering is performed (desktop, tablet, phone, console).

Like DirectX 12, Vulkan solves these problems by being a modern programming interface, correctly exploiting the resources of contemporary hardware. With Vulkan, the order the programmer transmits to the graphics card is much more complex. The translation process is therefore reduced to a minimum, thus resolving the uneven performance problem of both OpenGL and DirectX. However, this makes the use of Vulkan quite complex and therefore exclusive to experienced programmers.

## Lugdunum at a glance

Lugdunum is a 3D engine which is built around Vulkan. The engine also has the particularity to manage an illumination model that respects the laws of physics in order to obtain a photorealistic rendering (PBR). It uses the new 3D graphics file format, glTF 2.0, also designed by the Khronos Group.

It aims to be as cross-platform as possible, use a maximum of new technologies (Vulkan, C++17) while staying completely free and open-source, as a way of giving back to the community.

## Overview schematic

```google-drive
type: drawings
doc_id: 10oo8mQc44VgUc3K01SVYWPvHK6iFEDqcQDA0TnRHoy8
```
> [Overview of Lugdunum's components]{#fig:lugdunum-overview}