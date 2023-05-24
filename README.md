# Nano Node RPC Regression Test Tool

This tool is designed to provide a regression testing framework for the RPC commands between two versions of a Nano node. By comparing the JSON output of RPC commands between different versions, the tool can identify changes in command behavior and output format.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7 or higher
- pip

### Installation

First, clone this repository to your local machine:

```shell
git clone https://github.com/gr0vity-dev/nano-rpc-regression.git
cd nano-rpc-regression
```

Then, install the required Python packages using pip:

```shell
pip install -r requirements.txt
```

### Usage

You can run the regression test tool with the following command:

```shell
./differ.sh
```

The `FINAL_{v1}_{v2}.json` output file will be placed in a `compare_{v1}_{v2}/` directory in the root of the project. This file contains all the rpc mathods and its keys that differ between versions.

## How It Works

A dockerized nano-network with rpc enabled is created.
This tool executes a series of rpc calls against a node and reads the JSON output of RPC commands from two different versions of a Nano node, reformats the data into a unified structure, and writes the results to an output file. 

By comparing the reformatted JSON output, you can easily identify differences in the behavior of the RPC commands between the two versions. This can be especially useful for detecting unexpected changes or regressions in command behavior when upgrading to a new version of the Nano node.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
