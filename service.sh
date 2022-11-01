if [ -z $UPSTREAM_REPO ]

then
  echo "Cloning Main Branch [Lucifer]"
  git clone https://github.com/PR0FESS0R-99/LuciferMoringstar-Robot.git /LuciferMoringstar-Robot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /LuciferMoringstar-Robot

fi
cd /LuciferMoringstar-Robot
pip3 install -U -r requirements.txt
echo "Started Clone Version Lucifer...."
python3 main.py
