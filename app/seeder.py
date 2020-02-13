import sys
from subprocess import run

if len(sys.argv) == 2:
    n = int(sys.argv[1])

    for _ in range(n):
        run(["python", "app/manage.py", "seeddb"]) 
else:
    print('Invalid amount of arguments.')
    print('Syntax: python app/seeder.py <total>')
    sys.exit()