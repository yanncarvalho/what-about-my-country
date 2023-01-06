#!/usr/bin
ROOT_DIR=/usr/share/nginx/html

# Replace env vars in JavaScript files
echo "Replacing env constants in JS";
for file in $ROOT_DIR/assets/index-*.js
do
  echo "Processing $file ...";

    if [ ! -z $BACKEND_PORT ]
    then
       sed -Ei 's/(BACKEND_PORT:")[^"]*(",[_[:alnum:]]|"})/\1'$BACKEND_PORT'\2/' $file;
       echo "replace BACKEND_PORT=$BACKEND_PORT";
    fi

    if [ ! -z $BACKEND_ADDRESS ]
      then
        sed -Ei 's/(BACKEND_ADDRESS:")[^"]*(",[_[:alnum:]]|"})/\1'$BACKEND_ADDRESS'\2/' $file;
        echo "replace BACKEND_ADDRESS=$BACKEND_ADDRESS";
    fi

    if [ ! -z $BACKEND_PROTOCOL ]
    then
      sed -Ei 's/(BACKEND_PROTOCOL:")[^"]*(",[_[:alnum:]]|"})/\1'$BACKEND_PROTOCOL'\2/' $file;
      echo "replace BACKEND_PROTOCOL=$BACKEND_PROTOCOL";
    fi

    if [ ! -z $BACKEND_COUNTRY_ROUTE ]
    then
       sed -Ei 's/(BACKEND_COUNTRY_ROUTE:")[^"]*(",[_[:alnum:]]|"})/\1'$BACKEND_COUNTRY_ROUTE'\2/' $file;
       echo "replace BACKEND_COUNTRY_ROUTE=$BACKEND_COUNTRY_ROUTE";
    fi
done

nginx -g 'daemon off;'

