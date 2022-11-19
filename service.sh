if [ -z "https://github.com/PR0FESS0R-99/Midukki-RoBoT" ]

then
  echo "Successfully Cloned Midukki-RoboT"
  git clone https://github.com/PR0FESS0R-99/Midukki-RoBoT /Midukki-RoBoT 
else
  echo "Successfully Cloned Midukki-RoboT"
  git clone https://github.com/PR0FESS0R-99/Midukki-RoBoT /Midukki-RoBoT 

fi
cd /Midukki-RoBoT
pip3 install -U -r requirements.txt
echo "Started Clone Version Midukki...."
python3 main.py
