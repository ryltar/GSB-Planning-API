server='192.168.1.78'

cd ../

curl -X POST $server'/admin/employee-appointment?state=future' --header 'authorization: 123azerty456' --data 'id_employee=3'
