# nano-workspace
A workspace for Nano coin development

# Introduction
This project is targetted for the newbie Nano developer.
Most of the available help on the internet is targetted towards Nano operators.
There is not a lot of help for a software engineer/developer/programmer who wants to work with Nano.
This project is primarily for myself and also to help others who will follow after me.

IMPORTANT NOTE:
This project mostly ignores security and is focused on getting a node up and running as quickly and as easily as possible whilst building everything from scratch and everything installed locally within the nano-workspace folder. Having everything local allows for parallel projects on one computer. 

After spending a couple of days with Nano, my biggest problems were:
* It was a little confusing how to build the system. There is information on how to build the system but it is written for the experienced Nano developer and is not consice enough for Nano newbies. (https://docs.nano.org/integration-guides/build-options)
* There is no "hello world" like practice programs, it would be nice to introduce some trivial tools to play with and get some immediate feedback and leanring opportunities for newbies.
* Running a node gives very little feedback that makes any sense to a newbie, it would be nice to have a newbie mode with easy feedback and a page to explain the terminology used by the nano node logs.
* It is not easy to answer the question "is my node running well"?
* It is not easy to answer the question "is my node synced"?
* It is difficult to bootstrap the node (TODO: define bootstraping)
* It is not obvious how to circumvent bootstraping for a faster sync-up (https://docs.nano.org/running-a-node/ledger-management/#downloaded-ledger-files)
* It is not obvious how to setup a nano node locally within a disk directory (and hence allow for multiple parallel builds).

This project will try to provide solutions to the issues listed above.
The target audience is linux developers who are comfortable with makefiles. I currently run Ubuntu 20.04.

# Quick Terminology
| Term                 | Explanation   |
| -------------        | ------------- |
| Representative       | A representative is a voting peer as defined in the Nano whitepaper. |
| Frontier             | A frontier is the last block of a blockchain. | 
| Count (block_count)  | Block count is the number of checked blocked. Checked blocked are blocked that have been verified and are trusted. In a virgin system the block count start at 1. There is one block that is trusted, the genesis block. |
|  Unchecked           | Blocks that have been received but have not been checked yet. Initially, there is a large number of unchecked blocks and only one checked block because blocks cannot be checked until there is a chain of blocks that can lead to the genesis block, the only trusted block at the beggining. |
| Cemented             | TODO: I'll fill this in when I find out what it is :-) |

Nano glossary:  
There is an official Nano glossary and it can be found here:  
https://docs.nano.org/glossary

# Building Nano from scratch
This project consists of a Makefile in the root folder.
The purpose of that makefile is to build nano_node and its dependencies.

Currently it does the following:
* downloads and builds the boost library
* git clones the nano-node project and its subprojects
* builds nano-node

To do all the above, type 'make' to execute the default makefile target.

There are some other targets in the makefile for convenience:

## make get_ledger
Download the latest ledger from: https://mynano.ninja/api/ledger/download

It can be used to bootstrap a virgin node quickly without going through the extremely slow bootstrap process that takes days to complete usually.

NOTE: this step is totally insecure and shoudl only be used by people who do not deal with real coins or only risk small amounts of Nano.

## make force_ledger

Force copy the downloaded ledger into the data folder (this will overwrite the exisitng ledger in the data folder).

## make run_node
Run the nano node program with mostly default arguments. Use the folder 'data' to store the ledger data.

# Running the node
To start the node run 'make run_node'.
To stop the node, use the RPC script stop.sh in folder rpc/curl.
To get the block_count, use the script block_count.sh in folder rpc/curl.

# Useful links
* https://docs.nano.org/node-implementation/contributing
* https://docs.nano.org/running-a-node/ledger-management/#downloaded-ledger-files
* https://docs.nano.org/integration-guides/build-options

# TODO
* Learn about the beta network (https://docs.nano.org/running-a-node/beta-network)
* Learn about the test network (https://docs.nano.org/running-a-node/test-network)
