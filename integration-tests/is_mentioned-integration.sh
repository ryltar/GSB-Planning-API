server='192.168.1.78'

authorization='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6IlRydWUiLCJpZCI6IjU3IiwibmFtZSI6ImFkbXRlc3QgdGVzdCJ9.Bcp9_ftPiOiGjHycjY17KziWDPdy53VR_IrEtJyrD4s'

cd ../

jsonpost=$(curl --header 'authorization: '$authorization --data 'id=2&id_appointment=3' $server/admin/medics-mentioned)

medid=$(echo $jsonpost | cut -d ' ' -f 4)

echo $medid

echo 'post : ' $jsonpost

jsonput=$(curl -X PUT --header 'authorization: '$authorization --data 'id=3' $server/admin/medics-mentioned/$(echo $medid))

echo $jsonput

jsonget=$(curl --header 'authorization: '$authorization $server/admin/medics-mentioned/$(echo $medid))

echo $jsonget

jsongetall=$(curl --header 'authorization: '$authorization $server/admin/medics-mentioned)

echo $jsongetall

jsondelete=$(curl -X DELETE --header 'authorization: '$authorization $server/admin/medics-mentioned/$(echo $medid))

echo $jsondelete
