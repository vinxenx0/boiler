pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d app/translations -l en
pybabel init -i messages.pot -d app/translations -l es
