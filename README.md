# **Retector**

## *This is a simplified-securify2 for reentrancy detection*

# Installation

## Requirement

### Python (Version) = 3.7

### Soufflé (Version) = 1.6.2

### Solc (Version) >= 0.5.8

### Graphviz

## Install

```
sh install.sh
```
or
```
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

# Usage

## Notice

First of all, make sure you are also using python virtual enviroment if you installed retector in venv
```
source venv/bin/activate
```
If you are running for the first time and not using soufflé interpreter, set up LD_LIBRARY_PATH
```
cd <retector-dir>/reanalysis/libfunctors
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`
```
## Running detections to test.sol(Solc version 0.5.7)
```
retector test.sol
```
## Visualize CFG for test.sol
```
retector test.sol -v
```