download - copy một file từ server về local
scp root@192.168.1.99:/home/data/1.txt "C:\data\1.txt"

download - copy thư mục về máy local
scp -r root@192.168.1.99:/home/data /mycode/data01

upload - copy file (thư mục) từ local lên server
scp /mycode/3.txt root@192.168.1.99:/home/data/3.txt

scp -r /mycode/data root@192.168.1.99:/home/data
