import subprocess


def frama_focus_window_command(filename):
    result = subprocess.run(
        f'eval $(opam env) && frama-c -wp -wp-print {filename}',
        capture_output=True, text=True, shell=True)

    return result.stdout.split('\n'), result.stderr.split('\n')
