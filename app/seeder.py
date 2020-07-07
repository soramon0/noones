import sys
from subprocess import run

if len(sys.argv) == 2:
    n = int(sys.argv[1])

    for _ in range(n):
        try:
            run(["python", "manage.py", "seeddb"])
        except Exception as ex:
            print(ex)
    print('DONE SEEDING')

else:
    print('Invalid amount of arguments.')
    print('Syntax: python seeder.py <total>')
    sys.exit()
