# -*- mode: ruby -*-
# vi: set ft=ruby :

############################################################
# NYU: CSCI-GA.2820-001 DevOps and Agile Methodologies 
# Instructor: John Rofrano
############################################################
Vagrant.configure(2) do |config|
  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  # config.vm.box = "ubuntu/bionic64"
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.hostname = "ubuntu"

  # Forward Flask ports
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
  # Forward CouchDB ports
  config.vm.network "forwarded_port", guest: 5984, host: 5984, host_ip: "127.0.0.1"
  
  config.vm.network "private_network", ip: "192.168.33.10"

  # Windows users need to change the permission of files and directories
  # so that nosetests runs without extra arguments.
  # Mac users can comment this next line out
  config.vm.synced_folder ".", "/vagrant", mount_options: ["dmode=775,fmode=664"]

  ######################################################################
  # Provider for VirtualBox
  ######################################################################
  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
    vb.cpus = 1
    # Fixes some DNS issues on some networks
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  ############################################################
  # Provider for Docker
  ############################################################
  config.vm.provider :docker do |docker, override|
    override.vm.box = nil
    docker.image = "rofrano/vagrant-provider:ubuntu"
    docker.remains_running = true
    docker.has_ssh = true
    docker.privileged = true
    docker.create_args = ["-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro"]
    # docker.create_args = ["--platform=linux/arm64", "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro"]
  end

  ######################################################################
  # Copy some files to make developing easier
  ######################################################################

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

  ############################################################
  # Create a Python 3 environment for development work
  ############################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Update and install
    apt-get update
    apt-get install -y git tree wget vim python3-dev python3-pip python3-venv apt-transport-https libpq-dev
    apt-get upgrade python3
    pip3 install -U pip
    
    # Update pip and wheel so Python packages build correctly
    pip3 install wheel

    # Create a Python3 Virtual Environment and Activate it in .profile
    sudo -H -u vagrant sh -c 'python3 -m venv ~/venv'
    sudo -H -u vagrant sh -c 'echo ". ~/venv/bin/activate" >> ~/.profile'
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && cd /vagrant && pip install -r requirements.txt'
  SHELL

   ######################################################################
  # Add CouchDB docker container
  ######################################################################
  # docker run -d --name couchdb -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=pass couchdb
  config.vm.provision "docker" do |d|
    d.pull_images "couchdb"
    d.run "couchdb",
      args: "--restart=always -d --name couchdb -p 5984:5984 -v couchdb:/opt/couchdb/data -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=pass"
  end

  # ######################################################################
  # # Add PostgreSQL docker container
  # ######################################################################
  # # docker run -d --name postgres -p 5432:5432 -v psql_data:/var/lib/postgresql/data postgres
  # config.vm.provision :docker do |d|
  #   d.pull_images "postgres:alpine"
  #   d.run "postgres:alpine",
  #      args: "-d --name postgres -p 5432:5432 -v psql_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres"
  # end

  # ######################################################################
  # # Add a test database after Postgres is provisioned
  # ######################################################################
  # config.vm.provision "shell", inline: <<-SHELL
  #   # Create testdb database using postgres cli
  #   echo "Creating test database"
  #   sleep 10
  #   docker exec postgres psql -c "create database testdb;" -U postgres
  #   # Done
  # SHELL


  ######################################################################
  # Add CouchDB docker container
  ######################################################################
  # docker run -d --name couchdb -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=pass couchdb
  config.vm.provision "docker" do |d|
    d.pull_images "couchdb"
    d.run "couchdb",
      args: "--restart=always -d --name couchdb -p 5984:5984 -v couchdb:/opt/couchdb/data -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=pass"
  end

  ######################################################################
  # Setup a Bluemix and Kubernetes environment
  ######################################################################
  config.vm.provision "shell", inline: <<-SHELL
    echo "\n************************************"
    echo " Installing IBM Cloud CLI..."
    echo "************************************\n"
    # Install IBM Cloud CLI as Vagrant user
    sudo -H -u vagrant sh -c 'curl -sL http://ibm.biz/idt-installer | bash'
    sudo -H -u vagrant sh -c "echo 'source <(kubectl completion bash)' >> ~/.bashrc"
    # sudo -H -u vagrant sh -c "ibmcloud cf install --version 6.46.1"
    sudo -H -u vagrant sh -c "ibmcloud cf install"
    sudo -H -u vagrant sh -c "echo alias ic=/usr/local/bin/ibmcloud >> ~/.bash_aliases"
    echo "\n************************************"
    echo "If you have an IBM Cloud API key in ~/.bluemix/apiKey.json"
    echo "You can login with the following command:"
    echo "\n"
    echo "ibmcloud login -a https://cloud.ibm.com --apikey @~/.bluemix/apiKey.json -r us-south"
    echo "ibmcloud target --cf -o <your_org_here> -s dev"
    echo "\n************************************"
    # Show the GUI URL for Couch DB
    echo "\n"
    echo "CouchDB Admin GUI can be found at:\n"
    echo "http://127.0.0.1:5984/_utils"    
  SHELL

end


end
