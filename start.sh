if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/sachin9742s/Rocky_autofilter_Robot.git /Rocky_autofilter_Robot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Rocky_autofilter_Robot
fi
cd /Rocky_autofilter_Robot
pip3 install -U -r requirements.txt
echo "Starting Rocky_autofilter_Robot RoBot...."
python3 main.py
