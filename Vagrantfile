
Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"

  config.disksize.size = '20GB'

  config.vm.provider "virtualbox" do |v|
    v.name = "Tests"
    v.memory = "4096"
    v.cpus = 2
  end


  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get -y upgrade
    echo "Install pip and Python3.7 ******"
    sudo apt-get install -y python3-pip
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get -y install python3.7 
    python3.7 -m pip install --upgrade pip
    echo "Install Node v12******"
    curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
    sudo apt-get -y install nodejs
    echo "Install ffmpeg for Spleeter and ffmpeg******"
    sudo apt-get -y install ffmpeg
  SHELL
end

#fazer download de pretrained_models das releases - https://github.com/deezer/spleeter/releases/tag/v1.4.0