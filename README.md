# Kaufenbot Alarm System

  Generate alerts for price above/below a certain price for a cryptocurrency
  
![Web UI](/inputs/images/ui_ss.png)
 
## Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

  This repo is designed for generating alarms for cryptocurrincies using [ccxt](https://github.com/ccxt/ccxt).
  
## Requirements

* ccxt >= 1.56.59
* pandas >= 1.3.3
* streamlit >= 0.88.0

## Installation

```bash
git clone git@github.com:sefaburakokcu/kaufenbot-alarms.git
```
```bash
pip install -r requirements.txt
```

## Usage

Under __src__ folder, run commands below in parallel:

```bash
python backend.py
```
```bash
python sound.py
```
```bash
streamlit run ui.py
```

