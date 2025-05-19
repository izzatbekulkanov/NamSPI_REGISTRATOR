#!/bin/bash

# Fayl joylashgan papkaga o‘tamiz
cd "$(dirname "$0")"

# Virtual muhitni faollashtirish
source venv/bin/activate

# Daphne serverni ishga tushirish
exec daphne -b 0.0.0.0 -p 8000 Register.asgi:application
