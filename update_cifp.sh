#/bin/zsh

FILE=CIFP_230223.zip

cp -Rf ./app/cifp /tmp
rm -rf ./app/cifp/*
wget https://aeronav.faa.gov/Upload_313-d/cifp/${FILE} -O ./app/cifp/${FILE}
unzip ./app/cifp/$FILE -d ./app/cifp

