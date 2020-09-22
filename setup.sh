echo "## Checking Python Version:" &&
python3 -V &&
echo "" &&
echo "## Creating Virtual Environment:" &&
python3 -m virtualenv .venv &&
echo "" &&
echo "## Activating Virtual Environment:" &&
source .venv/bin/activate &&
echo "" &&
echo "## Checking Pip3 Version:" &&
pip3 -V &&
echo "" &&
echo "## Installing Project Dependencies:" &&
pip3 install -r requirements.txt &&
echo "" &&
echo "## Done!"
