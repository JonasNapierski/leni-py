# Leni-PY
Leni-PY or just Leni is a home assistant backend. Based on Flask it is designed to quickly extend your own assistant with simple Python modules. 

Leni is a project where everyone can participate. More information found in the [developer wiki](https://jonasnapierski.github.io/leni-py/)


## Installing
Leni requires git, python and pip:

Step 1: Download Source Code
```
$ git clone https://github.com/zirkumflexlab/leni-py
```

Step 2: Go into the Leni folder
```
$ cd leni-py
```

Step 3: Install all requirements using:
```
$ pip install -r requirements.txt
```

# Module
Leni offers a lot of modules, which still need to be installed separately. 

The installation of modules is done in 3 simple steps:
Step 1: make a modules folder
```
$ mkdir modules
```
Step 2: go into the folder
```
$ cd modules
```
Step 3: clone your favorite module
```
$ git clone  [the module of your choice]
```

Official Module:
 - [Weather-Module](https://github.com/jonasnapierski/weather-module) get your weather information with Leni
 - [Finnhub-Module](https://github.com/jonasnapierski/finnhub-module) intrested in stock! Get your stock-price

## Run
The easiest way to run Leni-PY is as below:
```
$ python Leni.py
```

