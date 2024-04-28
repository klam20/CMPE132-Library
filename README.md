# Library RBAC

## Table of Contents
- [Introduction](#introduction)
- [Developers](#developers)
- [Installation and Setup](#installation-and-setup)

## Introduction <a name="introduction"></a>

This is a library webpage that implements an RBAC model.
Certain roles have permissions that others role do not and the entire authorization process is based upon this.

**Developers**  <a name="developers"></a>
- Jeffrey Lam (@klam20)

## Installation and Setup  <a name="installation-and-setup"></a>
USING LINUX TERMINAL " > " denotes a Linux command
 <details>
    <summary> Install Python 3 and PIP </summary>
    &ensp; &ensp;&ensp; > sudo apt update <br>
    &ensp; &ensp;&ensp; > sudo apt install python3 <br>
    &ensp; &ensp;&ensp; > sudo apt install python3-pip
 </details>

 <details>
    <summary> Setting up virtualenv </summary>
    &ensp; &ensp;&ensp; > pip install virtualenv <br>
    &ensp; &ensp;&ensp; Create and enter into a directory which you want the virtual environment to be in <br>
    &ensp; &ensp;&ensp; Create the environment using > virtualenv [choose a name here for your virtualenv] <br>
    &ensp; &ensp;&ensp; Activate the environment using > source [name of virtualenv]/bin/activate <br>
    &ensp; &ensp;&ensp; If you want to deactivate the environment use > deactivate 
 </details>

  <details>
    <summary> Clone the repository </summary>
    &ensp; &ensp;&ensp; Create a directory that you want to clone the repository into <br>
    &ensp; &ensp;&ensp; Inside the directory run > git clone https://github.com/klam20/CMPE132-Library.git 
 </details>

<details>
    <summary> Install required dependencies within virtualenv </summary>
    &ensp; &ensp;&ensp; Change directory to the cloned directory CMPE132-Library <br>
    &ensp; &ensp;&ensp; Install libraries using > pip install -r requirements.txt 
 </details>

 <details>
    <summary> Using the application </summary>
    &ensp; &ensp;&ensp; Run the application using > python3 run.py <br>
    &ensp; &ensp;&ensp; Stop the application with CTRL + C
 </details>
