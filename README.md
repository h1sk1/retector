# **Retector**

## *This is a simplified-securify2 for reentrancy detection*

# Installation

## Requirements

* Python (Version) = 3.7

    You can manage python version with [pyenv](https://github.com/pyenv/pyenv) 

* Soufflé (Version) = 1.6.2

    You can follow instruction in [soufflé website](https://souffle-lang.github.io/install) 

    Or install manually

  1. Get the soufflé deb from github [releases](https://github.com/souffle-lang/souffle/releases)
        ```
        sudo dpkg -i <soufflé>
        ```
  2. If you are using ubuntu 20, you need to get [libffi6](http://mirrors.kernel.org/ubuntu/pool/main/libf/libffi/libffi6_3.2.1-8_amd64.deb)
        ```
        sudo dpkg -i <libffi6>
        ```
  3. Install dependencies
        ```
        sudo apt-get --fix-broken install
        ```

* Solc (Version) >= 0.5.7

    You can manage solc version with [py-solc-x](https://github.com/iamdefinitelyahuman/py-solc-x)

* Graphviz

    ```
    sudo apt-get install graphviz
    ```

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