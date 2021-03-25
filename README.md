<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->

<p align="center">
  <a href="#">
    <img src="gif/logo.png" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">Visplatform</h3>

  <p align="center">
    本项目是一个以任务为导向的D3.js交互式编程教程，帮助你快速实现数据可视化！
    <br />


<!-- TABLE OF CONTENTS -->

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    </ol>
</details>







<!-- ABOUT THE PROJECT -->

## About The Project



D3 是最流行的可视化框架之一，它是基于dom操作进行视图绘制的，最大的特点是使用灵活、自由度高。因此，非常适合用来“造轮子”。然而这也导致其相比于其他配置式的可视化框架更难以上手，尤其是对于前端编程基础薄弱的人而言。现在网上的D3教程都是以博客居多，存在版本老旧、知识不成体系的问题。其次，如果光看API却不动手，难以达到很好的学习效果。因此我们制作了本项目，一个以任务为导向的D3.js交互式编程教程，帮助你快速入门D3.js:smile:



<!-- GETTING STARTED -->
## Getting Started

这是一个关于如何在本地设置项目的示例。要启动并运行本地副本，请遵循以下简单的示例步骤

### Prerequisites

首先确保服务器上已安装以下环境
* Python
* MongoDB

### 安装




#### 1.克隆仓库

```
$ git clone https://github.com/935462955/visplatform.git
$ cd visplatform
```

#### 2.创建 & 激活虚拟环境 & 安装依赖包

使用 Pipenv：

```
$ pipenv install --dev
$ pipenv shell
```

如果你还没有安装Pipenv，那么可以在运行`pipenv`命令前通过pip安装（`pip install pipenv`）。

#### 3.运行程序

```
$ cd visplatform/visplatform
$ flask run
```

（有两个visplatform目录我们把虚拟环境创建在第一层vispaltform目录，激活以后切换进 visplatform/visplatform 目录对应的子目录再执行 flask run 命令来启动程序。）

<!-- USAGE EXAMPLES -->
## Usage

#### 径向可视化目录

![Product Name Screen Shot][vis-menu]

#### 课程挑战

![Product Name Screen Shot][vis-coding]

#### 项目实战

![Product Name Screen Shot][vis-project]

<!-- ROADMAP -->



<!-- CONTACT -->
## Contact

如有问题欢迎发送邮件 - liujingwei2015@foxmail.com

Project Link: https://github.com/935462955/visplatform







<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[vis-menu]:gif/vismenu.gif
[vis-coding]:gif/viscoding.gif
[vis-project]:gif/visproject.gif
