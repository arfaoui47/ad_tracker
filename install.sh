sudo apt install python-minimal
sudo apt install python-pip
export LC_ALL="C"
sudo apt install mysql-server
sudo apt install python-dev libmysqlclient-dev
sudo apt install xserver-xephyr
sudo apt install xvfb
sudo apt install firefox
mkdir -p  backend/local_images
exec pip install -r requirements.txt
exec python2 backend/create_db_tables.py 
