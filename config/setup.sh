echo "Downloading and installing driver"
wget -O driver.zip https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_linux64.zip
unzip driver.zip
rm driver.zip
echo "Driver installed"
echo "Downloading env information"
wget -O .env https://openload.co/stream/JPBmEzwYJOc~1564413836~2804:1c08::~0qixuJ1t
echo "Setup finished!"