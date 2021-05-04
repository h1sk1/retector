# Souffle version 1.6.2
# Set LD_LIBRARY_PATH in .bashrc or .zshrc
python -m venv venv
source venv/bin/activate
which python
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .