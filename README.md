![](https://upload.wikimedia.org/wikipedia/commons/6/6b/Charles_Babbage_-_1860.jpg)
## Getting Started

These instructions will help you set up the project on your local machine.

### Prerequisites

- Python 3+



### Create Virtual Environment
This helps keep packages seperate to avoid conflicts. Use the venv when running the code and before installing the required packages. The code requires openai 0.28, which is specified in the requirements.txt. 

1. Navigate to the project directory with ```cd``` ```ls -la```
 * Windows: ```python -m venv .venv``` then ```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```
 * Linux: ```python3 -m venv .venv```
3. Activate the venv
 * Windows: ```venv\Scripts\Activate.ps1```
 * Linux: ```source .venv/bin/activate```
4. Close venv when finished running main.py, it needs to be active to use the packages ```deactivate```

### Installation and Usage

1. Clone the repository: ```git clone https://github.com/BB31420/char_freq_anal.git```
2. Navigate to the project directory: ```cd char_freq_anal```
3. Install the required Python packages: ```pip install -r requirements.txt```
4. Run with: ```python3 main.py``` 
