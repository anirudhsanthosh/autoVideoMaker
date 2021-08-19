pip install wheel
pkg install libjpeg-turbo
pkg install termux-api
LDFLAGS="-L/system/lib/" CFLAGS="-I/data/data/com.termux/files/usr/include/" pip install Pillow
pip install -r requirements.txt