#/bin/zsh

FILE=CIFP_221229.zip

cp -Rf ./cifp /tmp
rm -rf ./cifp/*
wget https://aeronav.faa.gov/Upload_313-d/cifp/${FILE} -O ./cifp/${FILE}
unzip ./cifp/$FILE -d ./cifp

