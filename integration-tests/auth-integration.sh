server='192.168.1.78'

cd ../

curl --data 'passwd=test&email=test' $server/auth/token
