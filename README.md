# Inventory

[![Build Status](https://travis-ci.org/nyu-devops-summer-2021-inventory/inventories.svg?branch=master)](https://travis-ci.org/nyu-devops-summer-2021-inventory/inventories)
[![Codecov](https://codecov.io/gh/nyu-devops-summer-2021-inventory/inventories/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-devops-summer-2021-inventory/inventories/branch/master/graph/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

The inventory resource keeps track of how many of each product we have in our warehouse.

## Introduction

One of my favorite quote is:

"The greatest glory in living lies not in never falling, but in rising every time we fall." -Nelson Mandela

No, this quote has nothing to do with our project but it is still my favorite quote :D

The inventory resource keeps track of how many of each product we have in our warehouse. **At a minimum** it should reference a product and the quantity on hand. Inventory should also track restock levels and the condition of the item (i.e., new, open box, used). Restock levels will help you know when to order more products. Being able to query products by their condition (e.g., new, used) could be very useful.

## Prerequisite Installation using Vagrant
The easiest way to use start this service is with Vagrant and VirtualBox/Docker. If you don't have this software the first step is down download and install it. If you have an Mac with the M1 chip, you should download Docker Desktop instead of VirtualBox. Here is what you need:

Download: [Vagrant](https://www.vagrantup.com/)

Intel Download: [VirtualBox](https://www.virtualbox.org/)

Apple M1 Download: [Apple M1 Tech Preview](https://docs.docker.com/docker-for-mac/apple-m1/)

Install each of those. Then all you have to do is clone this repo and invoke vagrant:

### Using Vagrant and VirtualBox

```shell
git clone https://github.com/nyu-devops-summer-2021-inventory/inventories.git
cd inventories
vagrant up
```

### Using Vagrant and Docker Desktop

You can also use Docker as a provider instead of VirtualBox. This is useful for owners of Apple M1 Silicon Macs which cannot run VirtualBox because they have a CPU based on ARM architecture instead of Intel.

Just add `--provider docker` to the `vagrant up` command like this:

```sh
git clone https://github.com/nyu-devops-summer-2021-inventory/inventories.git
cd inventories
vagrant up --provider docker
```

This will use a Docker container instead of a Virtual Machine (VM). Everything else should be the same.

## Running the service for tests

You can now `ssh` into the virtual machine and run the service and the test suite:

```sh
vagrant ssh
cd /vagrant
```

You will now be inside the Linux virtual machine so all commands will be Linux commands.

## Manually running the Tests

Always run the test cases first!

Run the tests using `nosetests`

```shell
$ nosetests
```

Nose is configured via the included `setup.cfg` file to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

Nose is also configured to automatically run the `coverage` tool and you should see a percentage of coverage report at the end of your tests. If you want to see what lines of code were not tested use:

```shell
$ coverage report -m
```

You can also manually run `nosetests` with `coverage` (but `setup.cfg` does this already)

```shell
$ nosetests --with-coverage --cover-package=service
```

We've also include `pylint` in the requirements. If you use a programmer's editor like Atom.io you can install plug-ins that will use `pylint` while you are editing. This catches a lot of errors while you code that would normally be caught at runtime. It's a good idea to always code with pylint active.

When you are done, you can exit and shut down the vm with:

```shell
$ exit
$ vagrant halt
```

If the VM is no longer needed you can remove it with:

```shell
$ vagrant destroy
```

## Make calls to our services
- **GET /inventories** - Returns a list all of the inventories
- **GET /inventories/\<item-id>** - Returns the inventory with a given id number
- **POST /inventories** - creates a new inventory record in the database
- **PUT /inventories/\<item-id>** - updates a inventory record in the database
- **DELETE /inventories/\<item-id>** - deletes a inventory record in the database
- **GET /inventories/<item-id>/out-of-stock** - Given the id number, return if the inventory is out of stock
- **GET /inventories/<item-id>/in-stock** - Given the id number, return if the inventory is in stock