# LPix Gallery Mover

LPix is associated with the SA LP community. If you don't know what that is, there's nothing for you here.

## What does this do?
This repository contains a simple Python script that will move all files from one LPix gallery to another.
It is useful in case you're not happy anymore with how you divided your galleries and want to clean up a bit.

Due to how LPix works, all actual image links should keep working, so your LP updates won't break.

## How to install

It will be helpful if you know a bit on how to install python scripts and their dependencies.
I won't give specific advice here because this is dependent on your Operating System as well as your personal preferences.

You need the following prerequisites:
- Python 3
- pip for Python 3 in order to install dependencies.

The LPix Gallery mover requires several dependencies. Run the following on your command line to install them all:
```sh
pip install requests click browser-cookie3 beautifulsoup4
```

Download the script by [clicking on a Source Code link here](https://github.com/CO2-Codes/lpix-gallery-mover/releases/tag/1.0), and see if it runs. If everything works this should show a help page.
```sh
python lpixmove.py
```

## How to run

*The following section is a copy from the help page you get when running `python lpixmove.py`*

This is a very simple script. It will move all the files in one lpix gallery to another, assuming you are logged in to lpix in a supported browser and assuming you provide two valid gallery URLs that both belong to your account. IF YOU DO ANYTHING ELSE IT MAY BREAK IN UNEXPECTED WAYS, SUCH AS WIPING YOUR IMAGES FROM LPIX.

This script comes with ABSOLUTELY NO WARRANTY, you're on your own. Make sure to first test it on some unimportant data.

Note: Due to the way lpix works, the actual image URLs should not change, so none of your LP updates should break.

Usage example: 
```sh
python lpixmove.py move --old-gallery-url https://lpix.org/gallery/User+Name/12345 --new-gallery-url https://lpix.org/gallery/User+Name/98765
```

The URLs are exactly the ones your browser goes to if you click any of your galleries.

In case you want to use this script automatically, you can add the flag `--skip-confirmation` to the command to skip the manual confirmation prompt.
If you use `--skip-confirmation --delete-gallery` the old gallery will be automatically deleted if all images were moved successfully. For additional
scripting support, this script will stop with exit code 1 whenever any error was detected.

For all command line arguments please run python `lpixmove.py move --help`

## Troubleshooting

The script attempts to read your browser's cookies for your lpix password. If you're not logged in, logged in with multiple accounts, or use some kind of very unusual
browser, it might not work.

For any other issues, post in the Tech Support Fort and I'll try to help if I have time.


