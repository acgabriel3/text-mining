function gdrive_download() {
  CONFIRM=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://drive.google.com/uc?export=download&id=$1" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
  wget --load-cookies /tmp/cookies.txt "https://drive.google.com/uc?export=download&confirm=$CONFIRM&id=$1" -O $2
  rm -rf /tmp/cookies.txt
}

function move_to() {
  if [ ! -d $2 ] 
    then
      mkdir -p $2
  fi
  mv $1 $2 
}

# Allows to call a function based on arguments passed to the script
$*