<h1 align="center">Cyberpunk 2077 Breach Protocol Solution with Brute Force Algorithm</h1>
Cyberpunk 2077 Breach Protocol Solution with Brute Force Algorithm is an implementation of brute force algorithm to find the most optimal solution for the Breach Protocol minigame. This project is made with c++ for the heavy bruteforce processing, c++ for the cli, and python with PyQT5 for the GUI.

## ✨ Features
- Input values manually
- Input from txt files
- Auto generate input values
- Save optimal solution to folder

## 📖 How to run

### CLI
Simply double click to the bin/cli/cli.exe to run the cli.
Or run this with Command prompt
For Windows
```
bin/cli/cli.exe
```
For Linux
```
"bin/cli/cli - linux.exe"
```

### GUI
Simply double click to the bin/gui/gui.exe to run the gui.
Or run this with Command prompt
```
bin/gui/gui.exe
```


## 📘 Instruction

### Dependencies
Make sure to have python and c++ installed. Then navigate to ./src/gui and run with Command Prompt
```
pip install -r requirements.txt
```

### Compiling DLL
With command prompt
```
./compiledll
```
Or
```
g++ -shared -o "./src/lib/cracker.so" -fPIC "./src/lib/cracker.cpp" "./src/lib/structs/token.cpp" "./src/lib/structs/tokenslot.cpp" "./src/lib/structs/sequence.cpp" -O3
```
### Compiling CLI
With command prompt
```
./compilecli
```
Or
```
g++ -o "./bin/cli/cli" "./src/cli/cli.cpp" "./src/lib/cracker.cpp" "./src/lib/structs/token.cpp" "./src/lib/structs/tokenslot.cpp" "./src/lib/structs/sequence.cpp" -O3
```
### Compiling GUI
Please make sure to compile the dll file first before compiling the GUI.
With command prompt
```
./compilegui
```
Or
```
pyinstaller --workpath="./bin/gui" --distpath="./bin/gui" "src/gui/gui.spec"
```