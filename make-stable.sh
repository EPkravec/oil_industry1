#!/bin/bash
git pull
python version.py -p
python setup.py sdist upload -r https://beta.it-vend.ru:5550/pypi/
#python setup.py bdist_wheel --universal upload -r https://beta.it-vend.ru:5550/pypi/
git add .
git commit -m "up hwdriver master стабильная"
git push