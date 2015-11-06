Workshop MozFest 2015
==============================
**Content-Mining for Transparency of Drug Research**

Applying content mining tools to large corpora of scientific texts benefits researchers and the public through increased efficiency and transparency. With playground data from the field of drug trials and the help of ContentMine tools, we will explore how to create and visualize relations between entities, e.g. authors and companies, or drugs and diseases.

- Date: 7. November 2015
- Location: Ravensbourne @ London ([getting there](https://2015.mozillafestival.org/location))
- Host: [MozFest 2015](https://2015.mozillafestival.org/)
- Facilitators: 
	- Christopher Kittel ([@chris_kittel](https://twitter.com/chris_kittel))
	- Stefan Kasberger ([@stefankasberger](https://twitter.com/stefankasberger))
- Language: English
- [Pad](http://pads.cottagelabs.com/p/mozfest15)
- [Slides](http://www.slideshare.net/cheeseman1983/mozfest15-ws-contentmining-for-transparency-of-drug-research)
- [MozFest](https://schedule.mozillafestival.org/#_session-273)
- [ContentMine.org](http://contentmine.org/events/event/mozfest15-workshop/) 
- hashtag: [#mozfest](https://twitter.com/hashtag/MozFest?src=hash)

Please take 3 minutes and fill out our [evaluation form](https://docs.google.com/forms/d/13BsoUTHnYbYn1JDYyiF_pLbrxubgVKktvDzvkl7WCgM/viewform) after the workshop.

**ContentMine**
- [ContentMine.org](http://contentmine.org/)
- [@contentmine](http://twitter.com/thecontentmine)
- office@contentmine.org

![ContentMine Logo](CM_logo.png)

**Used Software**

Python [Anaconda](https://www.continuum.io/why-anaconda) with [Jupyter](http://jupyter.org/), [networkX](https://networkx.github.io/), [nltk](http://www.nltk.org/) and [beautifulsoup4](http://www.crummy.com/software/BeautifulSoup/)

You can find our code here:
- [code/MozFest2015.ipynb](code/MozFest2015.ipynb): Jupyter notebook
- [code/resources/analysis.py](code/resources/analysis.py): Functions for plotting and entitiy extraction. Have to be used with the stanford parser.
- [code/resources/readctree.py](code/resources/readctree.py): Classes for CProject and CTree.

**Used Data**

Open Access articles from the [Trials Journal](http://trialsjournal.com/) were used.

**Copyright**

Copyright-holder for all works is the [Shuttleworth Foundation](http://shuttleworthfoundation.org/).
- License for text, slides and images: CC BY 4.0
	- Except MozFest Logo
- License for code: MIT
- License of scientific articles from Trials Journal used as raw data: CC BY 4.0

## Schedule

| Time          | Agenda       | Description                                                            |
|---------------|--------------|------------------------------------------------------------------------|
| 10:45 - 11:15 | Introduction | Introduction into the workshop and ContentMine.                        |
| 11:15 - 12:15 | Hands-On     | Analyse and visualize the data with a Jupyter notebook in groups. |
| 12:15 - 13:00 | World Cafe   | Discuss ContentMining in groups.                                      |


## Copy data

We compiled a dataset and a folder with installers in advance and provide it offline during the workshop. Please copy the folder called *MozFest2015* into your preferred working directory or onto the desktop.

## Install Anaconda and jupyter notebook

We tested the installation on linux and windows, but not on Mac. It will install a number of Python 2.7 packages. If you already have the python packages nltk, networkx, beautifulsoup and ipython installed, you don't need to install anaconda.

Installers for the Anaconda environment and jupyter/ipython notebooks will be provided offline during the workshop, and can otherwise be downloaded from [here](https://www.continuum.io/downloads). Anaconda provides us with an easy to install environment, and includes the all software used for this workshop. You can use it for a a lot of fun purposes afterwards as well.

Installers can be found in the *anaconda* folder in the *Mozfest2015* folder.

**Mac OS**

On Mac OS, please use the installer called *Anaconda-MacOSX.pkg*. Run the installer and follow the instructions.

**Linux**

On Linux, open the terminal, navigate to the copied folder and into the *anaconda*-subfolder. In your terminal window execute for the correct bit version (you can find that under *System* -> *Settings* -> *Details* or via the terminal command *uname -m*):
```
bash Anaconda-Linux-32bit.sh 
```
or
```
bash Anaconda-Linux-64bit.sh 
```
Important: Type "bash" regardless of whether or not you are actually using the bash shell.

**Windows**

On Windows, please select the correct bit-version for your system (instruction how you can find that out which version you have are [here](http://windows.microsoft.com/en-us/windows7/find-out-32-or-64-bit)). You can look them up under *Start* -> Right Click *Computer* -> *Properties* -> System.

Double click either *Anaconda-Windows-32bit.exe* or *Anaconda-Windows-64bit.exe*.

### Start Jupyter notebook

The sessions starts with the most complicated thing - opening the notebook via the command line. So, open a new command line (terminal on Linux and Mac) and navigate to the copied folder. This is done by typing *cd DIR* (which stands for *change directory to DIR*).

```
cd your_working_directory/MozFest2015
```

Note: On Windows, folders are indicated by `\`, on Linux/Mac by `/`.

You can check whether you are in the right folder by typing `ls` (which stands for *list*) or on Windows `dir`. It prints a list of folder contents, if there is a file called *MozFest2015.ipynb*, you*re right.

Then type in `ipython notebook`, after which a new tab in your browser should open. In this tab, click on MozFest2015.ipynb and you finally arrived in the notebook.

## Contribute

We're happy you're thinking about contributing to ContentMine!

There are many ways to contribute:
- by reporting an issue regarding software or training
- by starting your own community
- by suggesting new features
- by writing code and documentation
- by closing issues
- by writing about the project

If you have questions, ask us directly at MozFest or write us a mail (mail ett stefankasberger dot at, web ett christopherkittel dot eu).

When you are online, you can find us:
- [contentmine.org](http://contentmine.org)
- [@thecontentmine](http://twitter.com/thecontentmine)
- office ett contentmine dot org

## Further materials
- [workshop Resources](https://github.com/ContentMine/workshop-resources): All resources for the ContentMine software toolchain - from getpapers and quickscrape over norma and AMI, this repository is the central source of tutorials for the ContentMine software pipeline.
- [Zotero](https://www.zotero.org/groups/contentmine): Public group with a collection of scientific papers and magazine articles relating to text data mining, copyright and ContentMine
- [Bipartite Graph @ Wikipedia](https://en.wikipedia.org/wiki/Bipartite_graph): explains the concept of bipartite networks and projection into unipartite networks.
- [Online Course: Python @ codecademy](https://www.codecademy.com/learn/python): Low-level introduction into programming with python.
- [Online Course: Introduction to Computer Science and Programming Using Python](https://courses.edx.org/courses/course-v1:MITx+6.00.1x_7+3T2015/info): 
- [Book: Python for Data Analysis](http://shop.oreilly.com/product/0636920023784.do): Very good introduction into Data Science with the Python modules iPython, pandas and numPy.

## Sources

## STRUCTURE
- [README.md](README.md): Overview of repository
- [code/MozFest2015.ipynb](code/MozFest2015.ipynb): Jupyter notebook
- [code/resources/analysis.py](code/resources/analysis.py): Functions for plotting and entitiy extraction. Have to be used with the stanford parser.
- [code/resources/readctree.py](code/resources/readctree.py): Classes for CProject and CTree.
- [assets/mozfest15.odp](assets/mozfest15.odp): Presentation
- [assets/mozfest15.pdf](assets/mozfest15.pdf): Presentation









