@echo off

echo ==============================
echo TAO MOI TRUONG VIRTUAL MOUSE
echo ==============================

py -3.11 -m venv .venv_hand

call .venv_hand\Scripts\activate.bat

python -m pip install --upgrade pip

pip install -r requirements.txt

echo.
echo ==============================
echo CAI DAT HOAN TAT
echo ==============================
echo Kich hoat moi truong bang:
echo .venv_hand\Scripts\activate

pause