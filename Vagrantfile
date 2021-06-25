# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant configuration for Inventories microservice
# Much of this code is borrowed from John Rofrano :)

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "ubuntu"

  # Configure IP address and port forwarding
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
  config.vm.network "private_network", ip: "192.168.33.10"

  # No windows users currently on the team
  # If you're running on Windows, uncomment the line below
  # config.vm.synced_folder ".", "/vagrant", mount_options: ["dmode=775,fmode=664"]

  # Provider configuration for Virtualbox (x86 only)
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 1
    # Fixes some DNS issues on some networks
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  # Provider for Docker (both x86 and ARM supported)
  config.vm.provider :docker do |docker, override|
    override.vm.box = nil
    docker.image = "rofrano/vagrant-provider:ubuntu"
    docker.remains_running = true
    docker.has_ssh = true
    docker.privileged = true
    docker.volumes = ["/sys/fs/cgroup:/sys/fs/cgroup:ro"]
    # Uncomment to force arm64 for testing images on Intel
    # docker.create_args = ["--platform=linux/arm64"]     
  end

  # Copy your .gitconfig file so that your git credentials are correct
  if File.exists?(File.expand_path("~/.gitconfig"))
    config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
  end

  # Copy your ssh keys for github so that your git credentials work
  if File.exists?(File.expand_path("~/.ssh/id_rsa"))
    config.vm.provision "file", source: "~/.ssh/id_rsa", destination: "~/.ssh/id_rsa"
  end

  # Copy your ~/.vimrc file so that vi looks the same
  if File.exists?(File.expand_path("~/.vimrc"))
    config.vm.provision "file", source: "~/.vimrc", destination: "~/.vimrc"
  end

  # Install OS packages via apt, configure virtual environment and install Python dependencies
  config.vm.provision "shell", inline: <<-SHELL
    echo "Installing OS packages for Python environment..."
    apt-get update
    apt-get install -y git tree wget vim python3-dev python3-pip python3-venv apt-transport-https
    apt-get upgrade python3
    
    echo "Installing PostgreSQL development library for arm64 architectures..."
    apt-get install -y libpq-dev

    echo "Configuring virtual environment and configuring auto activation in ~/.profile..."
    sudo -H -u vagrant sh -c 'python3 -m venv ~/venv'
    sudo -H -u vagrant sh -c 'echo ". ~/venv/bin/activate" >> ~/.profile'
    
    echo "Installing pip and wheel..."
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && pip install -U pip && pip install wheel'

    echo "Installing Python dependencies..."
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && cd /vagrant && pip install -r requirements.txt'      
  SHELL

  # Configure PostgreSQL docker container inside of Vagrant environment
  config.vm.provision :docker do |d|
    d.pull_images "postgres:alpine"
    d.run "postgres:alpine",
       args: "-d --name postgres -p 5432:5432 -v psql_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres"
  end

  # Configure a database for testing after PostgreSQL initializes
  config.vm.provision "shell", inline: <<-SHELL
    # Create testdb database using postgres cli
    echo "Pausing for 60 seconds to allow PostgreSQL to initialize..."
    sleep 60
    echo "Creating test database..."
    docker exec postgres psql -c "create database testdb;" -U postgres
  SHELL

end
