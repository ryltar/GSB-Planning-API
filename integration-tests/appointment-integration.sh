server='192.168.1.78'

authorization='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6IlRydWUiLCJpZCI6IjU3IiwibmFtZSI6ImFkbXRlc3QgdGVzdCJ9.Bcp9_ftPiOiGjHycjY17KziWDPdy53VR_IrEtJyrD4s'

cd ../

jsonpost=$(curl --header 'authorization: '$authorization --data 'start_date=01-01-2000&end_date=01-01-2000&state=0&feedback=lol&id_doctor=1' $server/admin/appointments) > /dev/null

medid=$(echo $jsonpost | cut -d ' ' -f 4)

echo $medid

echo 'post : ' $jsonpost

jsonput=$(curl -X PUT --header 'authorization: '$authorization --data 'feedback=lelz' $server/admin/appointments/$(echo $medid))

echo $jsonput

jsonget=$(curl --header 'authorization: '$authorization $server/admin/appointments/$(echo $medid))

echo $jsonget

jsongetall=$(curl --header 'authorization: '$authorization $server/admin/appointments)

echo $jsongetall

jsondelete=$(curl -X DELETE --header 'authorization: '$authorization $server/admin/appointments/$(echo $medid))

echo $jsondelete
