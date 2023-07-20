# z/OS Python Programs

## Description

This repository contains Python programs designed specifically for z/OS environment. These programs interact with z/OS datasets and functions.

## Features

- Dataset management: Reading, writing, deleting, and creating datasets.
- EBCDIC support: Handle EBCDIC encoding, common in mainframes.
- Python on Mainframe: Showcasing the use of Python on a z/OS system.

## Prerequisites

- Python 3 installed on z/OS.
- Access to z/OS system and necessary permissions to interact with z/OS datasets.

## Usage

Each script in this repository serves a different purpose. Here is how to run a typical script:

1. Transfer the script to your z/OS environment.
2. Make sure the script has execute permissions.
3. Run the script with the necessary command-line arguments. For example, if you're running a script that requires two datasets, you can use:
```bash
./script.py DATASET1 DATASET2
