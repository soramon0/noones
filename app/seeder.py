import sys
from subprocess import run
import platform

if len(sys.argv) == 2:
    n = int(sys.argv[1])
    system = platform.system()

    for _ in range(n):
        try:
            run(["python3", "app/manage.py", "seeddb"])
        except Exception:
            run(['bash', '.\\Scripts\\activate.bat', "&&" ,"python3", "app/manage.py", "seeddb"])
    print('DONE SEEDING')

else:
    print('Invalid amount of arguments.')
    print('Syntax: python3 app/seeder.py <total>')
    sys.exit()