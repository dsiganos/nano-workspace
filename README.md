# nano-workspace
A workspace for Nano coin development

# Introduction
This project is targetted for the newbie Nano developer.
Most of the available help on the internet is targetted towards Nano operators.
There is not a lot of help for a software engineer/developer/programmer who wants to work with Nano.
This project is primarily for myself and also to help others who will follow after me.

After spending a couple of days with Nano, my biggest problems were:
* It was a little confusing how to build the system. There is information on how to build the system but it is written for the experienced Nano developer and is not consice enough for Nano newbies.
* There is no "hello world" like practice programs, it would be nice to introduce some trivial tools to play with and get some immediate feedback and leanring opportunities for newbies.
* Running a node gives very little feedback that makes any sense to a newbie, it would be nice to have a newbie mode with easy feedback and a page to explain the terminology used by the nano node logs.
* It is not easy to answer the question "is my node running well"?
* It is not easy to answer the question "is my node synced"?
* It is difficult to bootstrap the node (TODO: define bootstraping)
* It is not obvious how to circumvent bootstraping for a faster sync-up

This project will try to provide solutions to the issues listed above.
The target audience is linux developers who are comfortable with makefiles. I currently run Ubuntu 20.04.

# Terminology

## Representative
A representative is a voting peer as defined in the Nano whitepaper.

## Frontier
A frontier is the last block of a blockchain.

## Count (block count)
Block count is the number of checked blocked. Checked blocked are blocked that have been verified and are trusted.
In a virgin system the block count start at 1. There is one block that is trusted, the genesis block.

## Unchecked
Blocks that have been received but have not been checked yet.
Initially, there is a large number of unchecked blocks and only one checked block because blocks cannot be checked until there is a chain of blocks that can lead to the genesis block, the only trusted block at the beggining.

## Cemented
TODO: I'll fill this in when I find out what it is :-)
