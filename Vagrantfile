
Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"

  config.vm.provider "virtualbox" do |v|
    v.name = "Tests"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    sudo apt-get -y upgrade
    echo "Install Python3 ******"
    sudo apt-get install -y python3-pip
    sudo apt-get install python3.7-dev python3.7
    python3.7 -m pipinstall --upgrade pip
    # echo "Install libsvm *******"
    # mkdir /vagrant/musicClass
    # cd /vagrant/musicClass
    # curl -LO 'http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/libsvm.cgi?+http://www.csie.ntu.edu.tw/~cjlin/libsvm+zip'
    # sudo apt-get install unzip
    # sudo unzip libsvm+zip -d libsvm
    # rm -r libsvm+zip
    # cd libsvm/libsvm-3.24/
    # make
  SHELL
end

# python3.7 -m pip install --no-cache-dir spleeter

# https://colab.research.google.com/github/deezer/spleeter/blob/master/spleeter.ipynb#scrollTo=ibXd-WCTpT0w

#fazer download de pretrained_models das releases - https://github.com/deezer/spleeter/releases/tag/v1.4.0