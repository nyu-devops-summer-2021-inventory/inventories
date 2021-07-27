# NYU DevOps Inventory Service (Summer 2021)
[![Build Status](https://travis-ci.com/nyu-devops-summer-2021-inventory/inventories.svg?branch=main)](https://travis-ci.com/nyu-devops-summer-2021-inventory/inventories)
[![codecov](https://codecov.io/gh/nyu-devops-summer-2021-inventory/inventories/branch/main/graph/badge.svg?token=OYHN2YOLX4)](https://codecov.io/gh/nyu-devops-summer-2021-inventory/inventories)

## Introduction

The inventory resource keeps track of how many of each product we have in our warehouse. It also includes details like SKU, restock levels, restock amounts, the condition of items, and whether or not an item is considered in-stock. 

## Installation of Vagrant, VirtualBox and Docker
The easiest way to develop this service is with Vagrant and VirtualBox (or if you're using an M1 MacBook, Docker). 

If you don't have this software the first step is down download and install it. 

Here is what you need:

- Both Intel and M1 CPUs need to install [Vagrant](https://www.vagrantup.com/)

- Intel devices should install [VirtualBox](https://www.virtualbox.org/)

- Apple M1 devices shoud install [Docker](https://docs.docker.com/docker-for-mac/apple-m1/)

Once you've installed these dependencies, you're ready to clone the repository and start developing!

### Developing Locally Using Vagrant

```shell
git clone https://github.com/nyu-devops-summer-2021-inventory/inventories.git
cd inventories
vagrant up
```

## Running the service for tests

You can now `ssh` into the virtual machine and run the service and the test suite:

```sh
vagrant ssh
cd /vagrant
```

You will now be inside the Linux virtual machine so all commands will be Linux commands.

## Manually running the Tests

Always run the test cases first!

First run the unit tests using `nosetests`:

```shell
$ nosetests
```

Then run the integration tests using `behave`:
```shell
$ honcho start &
$ behave
```

We've also include `pylint` in the `requirements.txt`. If you use a programmer's editor like VS Code you can install plug-ins that will use `pylint` while you are editing. This catches a lot of errors while you code that would normally be caught at runtime. It's a good idea to always code with pylint active.

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
- **PUT /inventories/\<item-id>/in-stock** - Update an item to "in stock" and send notifcations
