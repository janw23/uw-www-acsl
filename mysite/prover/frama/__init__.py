import pathlib
from subprocess import run
import sys

FRAMA_ROOT = pathlib.Path(__file__).resolve().parent


def _print_warning(msg):
    print('WARNING:', msg, file=sys.stderr)


def wp_print(fp):
    wp_print_script = FRAMA_ROOT / pathlib.Path('remote_wp_print.sh')
    assert wp_print_script.is_file()
    _print_warning('Frama runs on students via SSH')
    result = run(f'{wp_print_script} {fp}',
                 capture_output=True, text=True, shell=True)
    return result.stdout.split('\n'), result.stderr.split('\n')
