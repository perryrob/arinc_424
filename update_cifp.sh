#/bin/zsh
# https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/download/
FILE=CIFP_230323.zip

cp -Rf ./app/cifp /tmp
rm -rf ./app/cifp/*
wget https://aeronav.faa.gov/Upload_313-d/cifp/${FILE} -O ./app/cifp/${FILE}
unzip ./app/cifp/$FILE -d ./app/cifp

