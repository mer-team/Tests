echo "System update"
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

echo "Install MongoDB******"
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt-get update
sudo apt-get install -y mongodb

# INSTAL JAVA
# sudo apt install openjdk-15-jdk -y