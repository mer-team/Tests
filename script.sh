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