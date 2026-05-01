# Gacha SSR Simulator
A web-based probability analysis tool for gacha games. Select your game, input your current currency, and instantly see the expected pull count, cumulative probability curves, and a histogram showing your realistic odds of obtaining a high-rarity (SSR) character. Currently supports Fate/Grand Order and Uma Musume, with soft pity, hard pity, and rate-up mechanics all factored in.
Adding an screenshot or a mockup of your application in action would be nice.  

<img width="1540" height="726" alt="image" src="https://github.com/user-attachments/assets/6a89f48e-f5e8-4be4-9546-0199e07efe73" />

# How to run
Provide here instructions on how to use your application.   
- Download the latest binary from the Release section on the right on GitHub.  
### Option A — Python (local)
1. Clone: `git clone https://github.com/cis3296s26/final-project-03-gachaprobabilitymodel.git`
2. Enter the folder: `cd final-project-03-gachaprobabilitymodel`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the server: `python app.py`
5. Open a browser and go to `### Option A — Python (local)
1. Clone: `git clone https://github.com/cis3296s26/final-project-03-gachaprobabilitymodel.git`
2. Enter the folder: `cd final-project-03-gachaprobabilitymodel`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the server: `python app.py`
5. Open a browser and go to `[http://localhost:5001](http://10.0.0.55:5001)`

### Option B — Docker
1. `docker build -t gacha-sim .`
2. `docker run -p 5001:5000 gacha-sim`
3. Open a browser and go to `http://localhost:5001`

## Running tests
```bash
pip install pytest pytest-cov
pytest --cov=. --cov-report=term-missing
```

### Option B — Docker
1. `docker build -t gacha-sim .`
2. `docker run -p 5001:5000 gacha-sim`
3. Open a browser and go to `http://localhost:5001`

## Running tests
```bash
pip install pytest pytest-cov
pytest --cov=. --cov-report=term-missing
```

# How to contribute
Follow this project board to know the latest status of the project: https://github.com/cis3296s26/final-project-03-gachaprobabilitymodel.git

### How to build
- Use this github repository: https://github.com/cis3296s26/final-project-03-gachaprobabilitymodel
- Specify what branch to use for a more stable release or for cutting edge development.  
- Use Vscode
- Docker to develop the website
- Github for version control
- Specify additional library to download if needed 
- What file and target to compile and run. 
- What is expected to happen when the app start. 

Testing for commit
