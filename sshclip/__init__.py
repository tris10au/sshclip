from sshclip import devices

import pyperclip
import click
import time


def get_last_modified_time(device, clip_path):
    try:
        return device.stat(clip_path).st_mtime
    except FileNotFoundError:
        return None


def run_sshclip(device, clip_path=None, verbose=False, delay=1):
    if verbose:
        echo = click.echo
    else:
        echo = lambda s: None

    if clip_path is None:
        clip_path = device.find_clip_path()

    echo("[{name}] Starting SSHCLIP (write path: {path})".format(path=clip_path, name=device.NAME))

    previous_clipboard = pyperclip.paste() or ""
    previous_update = get_last_modified_time(device, clip_path)

    while True:
        latest_update = get_last_modified_time(device, clip_path)
        latest_clipboard = pyperclip.paste() or ""

        if latest_update is not None and (previous_update is None or previous_update < latest_update):
            previous_update = latest_update
            previous_clipboard = device.read(clip_path)
            pyperclip.copy(previous_clipboard)
            echo("Updating from other device: {0}".format(previous_clipboard))
        elif latest_clipboard != previous_clipboard and len(latest_clipboard) > 0:
            device.write(clip_path, latest_clipboard)
            previous_clipboard = latest_clipboard
            # A bug on macOS causes the clipboard to clear after 1 sec. Use the server to update it instead
            #previous_update = get_last_modified_time(device, clip_path)
            echo("Updating to other device: {0}, {1}, {2}".format(previous_clipboard, latest_clipboard, previous_update))

        time.sleep(delay)



@click.group()
def cli():
    pass


@cli.command()
@click.argument("host")
@click.argument("clip_path", default=None, required=False)
@click.option("--verbose/--no-verbose", default=False)
@click.option("--delay", default=1.11)
def client(clip_path=None, host=None, verbose=False, delay=1.11):  
    with devices.ClientDevice(host) as device:
        run_sshclip(device, clip_path, verbose, delay)


@cli.command()
@click.argument("clip_path", default=None, required=False)
@click.option("--verbose/--no-verbose", default=False)
@click.option("--delay", default=0.2)
def server(clip_path=None, verbose=False, delay=0.2):
    with devices.ServerDevice() as device:
        run_sshclip(device, clip_path, verbose, delay)
