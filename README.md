# Reminiscor
## Build and Run
- Install pipenv
```
pip install pipenv
```
- Install pyenv
```
cd ~
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
exec "$SHELL"
```
- Clone and Install Dependencies in a Virtual Environment
```
git clone https://github.com/Arjun-Somvanshi/Reminiscor
cd Reminiscor
pipenv install
```

- Run
```
# Working Directory is Reminiscor
pipenv shell
cd src
python main.py
```
