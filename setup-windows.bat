@echo off
cd %~dp0
echo Setting up virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Setup complete! Run the app using:
echo venv\Scripts\activate && python app.py
pause
