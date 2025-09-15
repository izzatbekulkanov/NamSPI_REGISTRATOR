# Fayl joylashgan papkaga o‘tamiz
Set-Location "C:\Users\Izunite\Documents\GitHub\NamSPI_REGISTRATOR\Register"

# Virtual muhitni faollashtiramiz
.\venv\Scripts\Activate.ps1

# Daphne serverni ishga tushiramiz
daphne -b 0.0.0.0 -p 8000 core.asgi:application