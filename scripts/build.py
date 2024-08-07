import os
import sys

CC = 'gcc'
CFLAGS = ['-lm', '-Wstringop-overflow=0']
ACTIONS = ['elf_rls', 'elf_dbg', 'driver_so']


def check_dirs():
    if os.path.exists('build'):
        return
    else:
        os.makedirs('build')


if __name__ == '__main__':
    check_dirs()
    if len(sys.argv) < 2:
        print(f"Missing action, ACTIONS={ACTIONS}")
        sys.exit(1)

    action = sys.argv[1]
    if action not in ACTIONS:
        print(f"Invalid action={action}, ACTIONS={ACTIONS}")
        sys.exit(1)

    if action == 'elf_dbg':
        out_dir = 'build/main'
        os.system(f"{CC} src/*.c {' '.join(CFLAGS)} -o {out_dir} -g")
        print(f"Output file: {out_dir}")
        sys.exit(0)

    if action == 'driver_so':
        lib_name = 'ltd_driver'
        out_dir = f'build/{lib_name}.so'
        os.system(f"{CC} src/{lib_name}.c {' '.join(CFLAGS)} -fPIC -shared -O3 -o {out_dir}")
        print(f"Output file: {out_dir}")
        sys.exit(0)
