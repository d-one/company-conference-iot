#!/bin/bash
USER_NAME=${1:-test1} # first parameter takes in the username, defaults to test1
PWD=${2:-$USER_NAME} # second parameter takes in the user pwd, defaults to the first parameter value
sudo apt-get --assume-yes install libssl-dev
sudo pkill -KILL -u $USER_NAME
sudo userdel $USER_NAME
sudo rm -rf /home/"$USER_NAME"
sudo adduser --disabled-password --gecos "" $USER_NAME # create specified user non-interactively
sudo usermod --password $(echo $PWD | openssl passwd -1 -stdin) $USER_NAME # set the password for the user
sudo adduser $USER_NAME sudo # assign sudo rights
echo $USER_NAME" ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/010_"$USER_NAME"-nopasswd # create a nopassword config for the user
sudo chmod u-w /etc/sudoers.d/010_"$USER_NAME"-nopasswd # remove write permissions after modification is done
sudo usermod -a -G gpio $USER_NAME
echo 'Creating venv for '$USER_NAME
sudo -i -u $USER_NAME python3 -m venv env
echo 'venv created'
echo 'Staring pip package installation'
sudo -i -u $USER_NAME ./env/bin/python -m pip install --upgrade pip
sudo -i -u $USER_NAME ./env/bin/python -m pip install RPi.GPIO AWSIoTPythonSDK boto3 azure-iot-device azure-iot-hub
echo $USER_NAME' configured!'
echo '...'
echo 'Testing the RPi.GPIO lib for '$USER_NAME
echo '...'
sudo cp ../python/gpio_test.py /home/$USER_NAME/gpio_test.py
result=$(sudo -i -u $USER_NAME ./env/bin/python /home/$USER_NAME/gpio_test.py 2>&1 >/dev/null)
sudo rm -rf  /home/$USER_NAME/gpio_test.py

hamster="RPi.GPIO installed and tested successfully!

      (\`-;\"-\"\`\`\`\"-;'-)
       \\\.'.       .'/'
       /             \\
       ;   ^     ^   ;
      /| -         - |\\\\
     ; \\\   '._Y_.'   / ;
    ;   \`-._ \\|/  _.-'  ;
   ;        \`\"\"\"\"\`       ;
   ;                     ;
   ;   \`\"\"\"-.   .-\"\"\"\`   ;
   /;  '--._ \\\ / _.--   ;\\\\
  :  \`.   \`/|| ||\\\`   .'  :
   '.  '-._       _.-'   .'
   (((-'  \`\"\"\"\"\"\`   \`'-)))"


if [ "$result" == "RPi.GPIO installed and tested successfully" ]; then
  echo -e "$hamster"
else
  echo $result
fi
