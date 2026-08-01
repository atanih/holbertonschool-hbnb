#!/bin/bash
# Verificacion completa de Part 3 - HBnB
API="http://127.0.0.1:5000/api/v1"
CT="Content-Type: application/json"
PASS=0; FAIL=0

chk () { # chk "desc" esperado obtenido
  if [ "$2" == "$3" ]; then
    echo "  OK   $1 ($3)"; PASS=$((PASS+1))
  else
    echo "  FAIL $1 (esperado $2, obtuve $3)"; FAIL=$((FAIL+1))
  fi
}

tok () { python3 -c "import sys,json;print(json.load(sys.stdin).get('access_token',''))"; }
jid () { python3 -c "import sys,json;print(json.load(sys.stdin).get('id',''))"; }

echo "=== TASK 2: JWT login ==="
ADMIN=$(curl -s -X POST $API/auth/login -H "$CT" -d '{"email":"admin@hbnb.io","password":"admin1234"}' | tok)
[ -n "$ADMIN" ] && { echo "  OK   admin login"; PASS=$((PASS+1)); } || { echo "  FAIL admin login"; FAIL=$((FAIL+1)); }
C=$(curl -s -o /dev/null -w "%{http_code}" -X POST $API/auth/login -H "$CT" -d '{"email":"admin@hbnb.io","password":"malo"}')
chk "credenciales invalidas -> 401" 401 $C
C=$(curl -s -o /dev/null -w "%{http_code}" $API/auth/protected)
chk "sin token -> 401" 401 $C

echo "=== TASK 4: solo admin crea usuarios ==="
U1=$(curl -s -X POST $API/users/ -H "Authorization: Bearer $ADMIN" -H "$CT" -d '{"first_name":"John","last_name":"Doe","email":"john@hbnb.io","password":"secret123"}')
ID1=$(echo "$U1" | jid)
[ -n "$ID1" ] && { echo "  OK   admin crea usuario"; PASS=$((PASS+1)); } || { echo "  FAIL admin crea usuario: $U1"; FAIL=$((FAIL+1)); }
U2=$(curl -s -X POST $API/users/ -H "Authorization: Bearer $ADMIN" -H "$CT" -d '{"first_name":"Jane","last_name":"Roe","email":"jane@hbnb.io","password":"secret123"}')
ID2=$(echo "$U2" | jid)

T1=$(curl -s -X POST $API/auth/login -H "$CT" -d '{"email":"john@hbnb.io","password":"secret123"}' | tok)
T2=$(curl -s -X POST $API/auth/login -H "$CT" -d '{"email":"jane@hbnb.io","password":"secret123"}' | tok)

C=$(curl -s -o /dev/null -w "%{http_code}" -X POST $API/users/ -H "Authorization: Bearer $T1" -H "$CT" -d '{"first_name":"X","last_name":"Y","email":"x@y.io","password":"secret123"}')
chk "usuario normal crea usuario -> 403" 403 $C

echo "=== TASK 4: solo admin crea amenities ==="
C=$(curl -s -o /dev/null -w "%{http_code}" -X POST $API/amenities/ -H "Authorization: Bearer $T1" -H "$CT" -d '{"name":"Sauna"}')
chk "usuario normal crea amenity -> 403" 403 $C
C=$(curl -s -o /dev/null -w "%{http_code}" -X POST $API/amenities/ -H "Authorization: Bearer $ADMIN" -H "$CT" -d '{"name":"Sauna"}')
chk "admin crea amenity -> 201" 201 $C

echo "=== TASK 3: places con ownership ==="
P=$(curl -s -X POST $API/places/ -H "Authorization: Bearer $T1" -H "$CT" -d '{"title":"Cozy Loft","description":"Nice","price":120,"latitude":40.41,"longitude":-3.70,"amenities":[]}')
PID=$(echo "$P" | jid)
[ -n "$PID" ] && { echo "  OK   usuario crea place"; PASS=$((PASS+1)); } || { echo "  FAIL crear place: $P"; FAIL=$((FAIL+1)); }
C=$(curl -s -o /dev/null -w "%{http_code}" -X POST $API/places/ -H "$CT" -d '{"title":"NoAuth","price":10,"latitude":0,"longitude":0}')
chk "crear place sin token -> 401" 401 $C
C=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $API/places/$PID -H "Authorization: Bearer $T2" -H "$CT" -d '{"title":"Hack","price":1,"latitude":0,"longitude":0}')
chk "editar place ajeno -> 403" 403 $C
C=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $API/places/$PID -H "Authorization: Bearer $T1" -H "$CT" -d '{"title":"Updated","price":150,"latitude":40.41,"longitude":-3.70}')
chk "dueno edita su place -> 200" 200 $C
C=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $API/places/$PID -H "Authorization: Bearer $ADMIN" -H "$CT" -d '{"title":"AdminEdit","price":99,"latitude":40,"longitude":-3}')
chk "admin salta ownership -> 200" 200 $C
C=$(curl -s -o /dev/null -w "%{http_code}" $API/places/)
chk "GET places publico -> 200" 200 $C
C=$(curl -s -o /dev/null -w "%{http_code}" $API/places/$PID)
chk "GET place detalle publico -> 200" 200 $C

echo "=== TASK 3: reviews con reglas de negocio ==="
C=$(curl -s -o /dev/null -w "%{http_code}" -X POST $API/reviews/ -H "Authorization: Bearer $T1" -H "$CT" -d "{\"text\":\"Mio\",\"rating\":5,\"place_id\":\"$PID\"}")
chk "resenar tu propio place -> 400" 400 $C
R=$(curl -s -X POST $API/reviews/ -H "Authorization: Bearer $T2" -H "$CT" -d "{\"text\":\"Genial\",\"rating\":5,\"place_id\":\"$PID\"}")
RID=$(echo "$R" | jid)
[ -n "$RID" ] && { echo "  OK   otro usuario resena"; PASS=$((PASS+1)); } || { echo "  FAIL crear review: $R"; FAIL=$((FAIL+1)); }
C=$(curl -s -o /dev/null -w "%{http_code}" -X POST $API/reviews/ -H "Authorization: Bearer $T2" -H "$CT" -d "{\"text\":\"Otra vez\",\"rating\":4,\"place_id\":\"$PID\"}")
chk "segunda review del mismo user -> 400" 400 $C
C=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $API/reviews/$RID -H "Authorization: Bearer $T1" -H "$CT" -d '{"text":"Hack","rating":1}')
chk "editar review ajena -> 403" 403 $C
C=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $API/reviews/$RID -H "Authorization: Bearer $T2" -H "$CT" -d '{"text":"Editada","rating":4}')
chk "autor edita su review -> 200" 200 $C
C=$(curl -s -o /dev/null -w "%{http_code}" $API/places/$PID/reviews)
chk "GET reviews de un place publico -> 200" 200 $C

echo "=== TASK 3/4: users ==="
C=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $API/users/$ID1 -H "Authorization: Bearer $T2" -H "$CT" -d '{"first_name":"Hack"}')
chk "editar otro usuario -> 403" 403 $C
C=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $API/users/$ID1 -H "Authorization: Bearer $T1" -H "$CT" -d '{"email":"nuevo@hbnb.io"}')
chk "usuario cambia su email -> 400" 400 $C
C=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $API/users/$ID1 -H "Authorization: Bearer $T1" -H "$CT" -d '{"first_name":"Johnny"}')
chk "usuario edita su nombre -> 200" 200 $C
C=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $API/users/$ID1 -H "Authorization: Bearer $ADMIN" -H "$CT" -d '{"email":"john2@hbnb.io","password":"nuevapass"}')
chk "admin cambia email y password -> 200" 200 $C
C=$(curl -s -o /dev/null -w "%{http_code}" -X PUT $API/users/$ID1 -H "Authorization: Bearer $ADMIN" -H "$CT" -d '{"email":"jane@hbnb.io"}')
chk "admin pone email duplicado -> 400" 400 $C

echo "=== TASK 1: password nunca expuesto ==="
if curl -s $API/users/ | grep -q '"password"'; then
  echo "  FAIL password expuesto"; FAIL=$((FAIL+1))
else
  echo "  OK   password no aparece en GET"; PASS=$((PASS+1))
fi

echo
echo "==================================="
echo "  PASARON: $PASS   FALLARON: $FAIL"
echo "==================================="
