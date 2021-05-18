import pathlib
from subprocess import run

FRAMA_ROOT = pathlib.Path(__file__).resolve().parent


def wp_print(fp):
    wp_print_script = FRAMA_ROOT / pathlib.Path('remote_wp_print.sh')
    assert wp_print_script.is_file()
    cmd = f'{wp_print_script} {fp}'
    result = run(f'{wp_print_script} {fp}',
                 capture_output=True, text=True, shell=True)
    return result.stdout.split('\n'), result.stderr.split('\n')
