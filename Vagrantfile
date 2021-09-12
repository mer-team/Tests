Vagrant.configure("2") do |config|

  # operating system
  config.vm.box = "ubuntu/xenial64"
  
  # plugin vagrant-disksize to resize disk storage
  config.disksize.size = '20GB'

  # rabbitmq management port
  config.vm.network "forwarded_port", guest: 15672, host: 15672

  config.vm.provider "virtualbox" do |v|
    v.name = "Tests"
    v.memory = "6000"
    v.cpus = 4
  end

  config.vm.provision "shell", path: "script.sh"
end