server='192.168.1.78'

authorization='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6IlRydWUiLCJpZCI6IjU3IiwibmFtZSI6ImFkbXRlc3QgdGVzdCJ9.Bcp9_ftPiOiGjHycjY17KziWDPdy53VR_IrEtJyrD4s'

cd ../

jsonemp=$(curl --header 'authorization: '$authorization --data 'lastname=dupont&firstname=auguste&is_admin=t&passwd=azerty&email=adupont@adup.dup&num_tel=0101010101&pseudo=wallah' $server/admin/employees)

empid=$(echo $jsonemp | cut -d ' ' -f 4)

jsonadd=$(curl --header 'authorization: '$authorization --data 'num=2&street=lol&codepost=62000&city=arras&country=france&indication=lol' $server/admin/addresses)

jsonpost=$(curl --header 'authorization: '$authorization --data 'lastname=dupont&firstname=auguste&email=adupont@adup.dup&num_tel=0101010101&id_employee=3&id_address=2&id_specialty=2' $server/admin/doctors)

medid=$(echo $jsonpost | cut -d ' ' -f 4)

echo $medid

echo 'post : ' $jsonpost

jsonput=$(curl -X PUT --header 'authorization: '$authorization --data 'lastname=hadim' $server/admin/doctors/$(echo $medid))

echo $jsonput

jsonget=$(curl --header 'authorization: '$authorization $server/admin/doctors/$(echo $medid))

echo $jsonget

jsongetall=$(curl --header 'authorization: '$authorization $server/admin/doctors)

echo $jsongetall

jsondelete=$(curl -X DELETE --header 'authorization: '$authorization $server/admin/doctors/$(echo $medid))

echo $jsondelete
