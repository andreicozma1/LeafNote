# 0x432d2d


## Download the Source Code

1. Clone the Repository 
```
git clone https://github.com/UTK-CS340-Fall-2020/0x432d2d.git
cd 0x432d2d
```

## Install Dependencies
Recommended: Use the setup script!
2. Create a Virtual Environment
```
python3 -m virtualenv .venv
```

3. Activate the Virtual Environment
```
source .venv/bin/activate (Linux/macOS)
.venv\Scripts\activate.bat (Windows)
```

4. Install the Dependencies
Recommended: Use the run script!
```
pip3 install -r requirements.txt
```

## Run Program Directly
If you want to run the application directly from the command line, first follow the previous steps then run this command.
```
fbs clean && fbs run
```

## Create Standalone Installer
If you would like to download the application, first follow the previous steps then run this command to create the installer package. 
```
fbs freeze && fbs installer 
```
This will create the packages and save them into the target folder.

## Install
In order to install the application onto your system use the following commands depending on your operating system.

- Linux 
```
sudo dpkg -i target/LeafNote.deb
```

- Mac
```
open target/LeafNote.dmg
```

- Windows
```
start target\LeafNote.exe
```
