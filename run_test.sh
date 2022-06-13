pyclean .

coverage run --source=hvzn -m pytest -v tests && coverage report -m

pyclean .
