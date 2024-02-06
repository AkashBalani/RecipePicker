# init-container.sh

#!/bin/bash

# echo "Current directory: $(pwd)"
# ls -la /app

python manage.py makemigrations
python manage.py migrate
