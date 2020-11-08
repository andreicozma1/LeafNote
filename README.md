# LeafNote

## 1. Setup
1. Clone Repository 
```
git clone https://github.com/UTK-CS340-Fall-2020/0x432d2d.git
cd 0x432d2d
```

- Ensure your current directory is the one that contains the *requirements.txt* file
- Recommended: Use the *setup.sh* script (Linux and macOS only)!   
2. Create a Virtual Environment
```
python3 -m virtualenv .venv
```

3. Activate the Virtual Environment
```
source .venv/bin/activate (Linux/macOS)
.venv\Scripts\activate.bat (Windows)
```

4. Install Dependencies
```
pip3 install -r requirements.txt
```

## 2. Run LeafNote
- Requirements: Run all Setup steps
- Recommended: Use the *run.sh* script (Linux and macOS only)!   
```
python3 src/main.py (Linux/macOS)
python3 src\main.py (Windows)
```

## 3. Run Tests
- Requirements: Run all Setup steps
- Recommended: Use the *test.sh* script (Linux and macOS only)!   
```
cd src
python3 -m unittest
```