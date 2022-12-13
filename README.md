# nano-workspace
A workspace for Nano coin development

# Introduction
This project is targetted for the newbie Nano developer. Most of the available help on the internet is targetted towards Nano operators and there is not a lot of help for a software engineer/developer who wants to work inside Nano node. This project is primarily for myself, to document my journey with Nano, and also to help others who follow on a similar path.

Think of this project as a guide to Nano development from a nano node software engineer's perpective (C++ perspective) as opposed to a software engineer that plans to integrate other software with nano node (RPC perspective).

This project is work in progress.

IMPORTANT NOTE:
This project initially mostly ignores security and is focused on getting a node up and running as quickly and as easily as possible whilst building everything from scratch and everything installed locally within the nano-workspace folder. Having everything local allows for parallel projects on one computer. This project is focused on learning the software architecture of nano node and not on operational issues such as operational security.

After spending a couple of days with Nano, my biggest problems were:
* It was a little confusing how to build the system, it took me a few hours to find my bearings. There is information on how to build the system but it is written for the experienced Nano developer and is not consice enough for Nano newbies (<https://docs.nano.org/integration-guides/build-options>). This project documents and automates the building of nano node with mostly default options.
* There is no "hello world" like practice programs, it would be nice to introduce some trivial tools to play with and get some immediate feedback and leanring opportunities for newbies. This project aims to create a set of hello-world like programs for experiementation and learning.
* Running a node gives very little feedback that makes any sense to a newbie, it would be nice to have a newbie mode with easy feedback and a page to explain the terminology used by the nano node logs. 
* It is not easy at first to answer the question "is my node running well"?
* It is not easy at first to answer the question "is my node synced"? ([is_synced.py](rpc/python/is_synced.py))
* It is difficult to bootstrap the node (TODO: define bootstraping)
* It is not obvious how to circumvent bootstraping for a faster sync-up (https://docs.nano.org/running-a-node/ledger-management/#downloaded-ledger-files).
* It is not obvious how to setup a nano node locally within a disk directory so that all the relevant data is within a well-defined space and easy to find and track. Having all the data locally also allows for multiple parallel builds.

This project will try to provide solutions to the issues listed above. The target audience is linux developers who are comfortable with makefiles. I currently run Ubuntu 20.04.

# Quick Terminology
| Term                 | Explanation   |
| -------------        | ------------- |
| Representative       | A representative is a voting peer as defined in the Nano whitepaper. |
| Frontier             | A frontier is the last block of a blockchain. | 
| Count (block_count)  | Block count is the number of checked blocked. Checked blocked are blocked that have been verified and are trusted. In a virgin system the block count start at 1. There is one block that is trusted, the genesis block. |
|  Unchecked           | Blocks that have been received but have not been checked yet. Initially, there is a large number of unchecked blocks and only one checked block because blocks cannot be checked until there is a chain of blocks that can lead to the genesis block, the only trusted block at the beggining. |
| Confirmed            | A block becomes confirmed when its election reaches quorum. This doesn't necessarilly mean the block is also cemented. |
| Cemented             | Cemented blocks are confirmed blocks that also have their confirmation height set and are saved in the ledger. |
| Root (of block)      | The root of a block is the previous block, except for open blocks, where it is the account public key. |

Nano glossary:  
There is an official Nano glossary and it can be found here:  
https://docs.nano.org/glossary

# Building Nano from scratch
This project consists of a Makefile in the root folder.
The purpose of that makefile is to build nano_node and its dependencies.

Currently it does the following:
* downloads and builds the boost library
* git clones the nano-node project and its subprojects
* builds nano-node, Qt wallet and self test executables
* optionally downloads a ledger for fast bootstrapping
* shows how to enable_control for RPCs
* integrates with Visual Studio Code (look inside the .vscode folder for settings)

Before building the software, ensure you have these dependencies installed (for ubuntu 20.04):  
```apt-get install make cmake git p7zip-full g++ qt5-default```.

On Ubuntu 21 and above instead of qt5-default, install:  
```qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools```

To build the software, type 'make' to execute the default makefile target or start VSCode at the top directory and do a cmake build.

There are some other targets in the makefile for convenience and documentation purposes:

## make get_ledger
Download the latest ledger from: https://mynano.ninja/api/ledger/download

It can be used to bootstrap a virgin node quickly without going through the extremely slow bootstrap process that takes days to complete usually.

NOTE: this step is totally insecure and shoudl only be used by people who do not deal with real coins or only risk small amounts of Nano.

## make force_ledger

Force copy the downloaded ledger into the nano-node/data folder (this will overwrite the exisitng ledger in the data folder).

## make run_node
Run the nano node program with mostly default arguments. Use the folder 'data', inside nano-node, to store the ledger.

## make tail_logs
Runs a tail command in the logs folder.

## make enable_control
Sets the RPC enable_control flag.

# Running the node
To start the node run 'make run_node'.  
To stop the node, use the RPC script stop.sh in folder rpc/curl.  
To get the block_count, use the script block_count.sh in folder rpc/curl.  
Nano node produces log output which can be found in nano-node/data/log folder.

# Downloading a ledger and jump-starting nano node
If you start a nano node from scratch, it will take many days to catch up with the network and there is a chance the it will get stuck after many days of effort. It is not practical to wait that long. The solution is to jump start the nano node. We do that by downloading an already populated ledger database file.
One can be got from <https://mynano.ninja/api/ledger/download>.
The [Makefile](Makefile) automates the process of downloading and installing the ledger.
To install the latest ledger, run the commands but first ensure that nano_node is not running:
```
rpc/curl/stop.sh
<wait until nano_node is stopped>
make get_ledger
make force_ledger
```
More details about ledger management can be found [here](https://docs.nano.org/running-a-node/ledger-management/#downloaded-ledger-files).

# Node synced
Once your node starts running, the first questions you are likely to have are:
* is my node progressing?
* is my node synced?

You can check the progress of your node by check the block counts [block_count.py](rpc/python/block_count.py).  
You want to see your counters increasing steadily.  
You can also look at the log files in the data directory.

To check if your node is synced, is less straightforward because there is no authoritative way to say you are synced.  
However, you can make a educated estimate according to your view of the network.  
The script [is_synced.py](rpc/python/is_synced.py) shows one way of doing that.

# RPC
The nano node runs an HTTP server on http://[::1]:7076 and listens for incoming requests.  
Requests and responses are in the form of json over HTTP.  
A raw TCP dump of a simple request/response can be seen [here](examples/captures/block_count_req_resp.txt).

A number of trivial but useful scripts are in the [rpc](rpc) folder.
There are scripts written using shell scripting and curl in the [curl](rpc/curl) folder and also python scripts in the [python](rpc/python) folder.
The script [block_count.py](rpc/python/block_count.py) is a trivial script that shows how to do a trivial RPC.
The [telemetry.py](rpc/python/telemetry.py) script is a step-up from block_count.py and showing how to manipulate the data returned.

# Creating a wallet and accounts
Once you have a node up and running and synced, you will want to create a wallet.  
A wallet is not a Nano network concept. The network does not track nor reference wallets.
A wallet is made of a wallet ID and a secret seed.  
The script [wallet_create.py](rpc/python/wallet_create.py) shows how to create wallets.  
Wallets can be destroyed with [wallet_destroy.py](rpc/python/wallet_destroy.py)

Wallets can hold accounts; the scripts below show how to create, list and remove accounts using the scripts:
* [account_create.py](rpc/python/account_create.py)
* [account_list.py](rpc/python/account_list.py)
* [account_remove.py](rpc/python/account_remove.py)

Each account has its own blockchain. To transfer nanos, a send block is created on the originating blockchain and that money is removed forever from its balance. That money is now in transit to the receiver. The receiver needs to create a receive block to receive the money. He can do this whenever or even never (burned money). A blockchain consists of a seriers of blocks. A block is made of the following fields:

| Field | Explanation |
|-------|-------------|
| type            | This currently always set to "state", in the past other types were used too. |
| subtype         | Thsi is optional and can be one of: "receive", "send", "change", "epoch". |
| account         | The Nano for which the block is created. |
| previous        | Hash of previous block in blockchain. |
| representative  | The Nano Account to use as representative. |
| balance         | Current balance of the Nano Account once the block is confirmed across the Nano Network. It is formatted in “raw” units. |
| link            | Link depends on context. For send blocks it contains the public key of the receiver. For receive blocks, it contains the hash of the associated send block. For epoch blocks, it is set to a specific string. |
| link_as_account | address of corresponding account. |
| signature       | A signature to validate the integrity of the Nano Block and prove it is sent by the blockchain owner. |
| work            | Proof-of-work algorithm that performs the function of spam avoidance |

There are a lot of denominations of nano but for our purposes at this stage, only 2 need to be known, NANO/MNano which is equal to 2^30 raw nanos.



A much better explanations of wallets, accounts, nanos and blocks is [here](https://medium.com/nanocurrency/getting-started-developing-with-nano-currency-part-1-build-your-foundation-cec2013657e1).

Note that you can't destroy an account once it is in the network.

# Using Visual Studio Code to build and debug
The project is also setup to work with vscode. The vscode files are in ".vscode". Vscode does not share the build directory with the makefile. The makefile builds in folder "build" whereas vscode builds in "vsbuild". The two build directories can coexist.

# Useful links
* https://docs.nano.org/node-implementation/contributing
* https://docs.nano.org/running-a-node/ledger-management/#downloaded-ledger-files
* https://docs.nano.org/integration-guides/build-options
* https://docs.nano.org/node-implementation/contributing/#wip-developer-starter-pack
* https://blog.nano.org/getting-started-developing-with-nano-currency-part-1-build-your-foundation-cec2013657e1
* https://blog.nano.org/getting-started-developing-with-nano-currency-part-2-interacting-with-public-and-private-nano-adb98ef57fbf
* http://nanoo.tools
* https://crates.io/crates/feeless (Rust tools and node for Nano)
* https://nano.community/getting-started-devs/protocol-reference (notes/help about C++ source code)
* https://beta.nanocrawler.cc
* http://peers.siganos.xyz

# TODO
* Learn about the beta network (https://docs.nano.org/running-a-node/beta-network)
* Learn about the test network (https://docs.nano.org/running-a-node/test-network)
