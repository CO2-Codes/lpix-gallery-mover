# MIT License
#
# Copyright (c) 2024 CO2-Codes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import re
import requests
import browser_cookie3
import click
from bs4 import BeautifulSoup


def delete_old_gallery(old_gallery_id, user_gallery_url, cookies):
    try:
        form_data = {'galleryid': old_gallery_id,
                     'confirmdelgal': 'Confirm+Delete'}
        delete_response = requests.post(
            user_gallery_url, cookies=cookies, data=form_data)
        if delete_response.status_code == 200:
            click.echo(f'Successfully deleted gallery {old_gallery_id}.')
        else:
            click.echo(
                f'Something went wrong while deleting gallery {old_gallery_id}. Got http status code {delete_response.status_code} with message {delete_response.text}.')
            sys.exit(1)
    except Exception as e:
        click.echo(
            f'Something went wrong while deleting gallery {old_gallery_id}. Got exception {e}.')
        sys.exit(1)


def parse_page(gallery_url, type_for_logging, cookies):
    try:
        gallery_id = re.findall(r'/\d+', gallery_url)[-1][1:]

        # Need to know the gallery without the last part for the deletion URL.
        # To deal with the edge case where a gallery id is the same as the user name, use a workaround to only remove
        # the last occurrence.
        index_gallery_id = gallery_url.rindex(gallery_id)
        user_gallery = gallery_url[:index_gallery_id]
    except:
        click.echo(
            f"ERROR: Cannot read id from {type_for_logging} gallery URL.")
        sys.exit(1)

    html_page = requests.get(gallery_url, cookies=cookies)
    soup = BeautifulSoup(html_page.text, 'html.parser')
    try:
        gallery_title = soup.find('h2').text
    except:
        click.echo(
            f"Something went wrong. Possibly gallery {gallery_url} does not exist. This script cannot currently create galleries for you.")
        sys.exit(1)

    return {'gallery_title': gallery_title, 'gallery_id': gallery_id, 'parsed_html': soup, 'user_gallery_url': user_gallery}


@click.group()
def cli():
    """   This is a very simple script. It will move all the files in one lpix gallery to another, assuming you
          are logged in to lpix in a supported browser and assuming you provide two valid gallery URLs that both belong
          to your account. IF YOU DO ANYTHING ELSE IT MAY BREAK IN UNEXPECTED WAYS, SUCH AS WIPING YOUR IMAGES FROM LPIX.

          This script comes with ABSOLUTELY NO WARRANTY, you're on your own. Make sure to first test it on some unimportant data.

          Note: Due to the way lpix works, the actual image URLs should not change, so none of your LP updates should break.

          Usage example:
          python lpixmove.py move --old-gallery-url https://lpix.org/gallery/User+Name/12345 --new-gallery-url https://lpix.org/gallery/User+Name/98765

          The URLs are exactly the ones your browser goes to if you click any of your galleries.

          In case you want to use this script automatically, you can add the flag --skip-confirmation to the command
          to skip the manual confirmation prompt. If you use --skip-confirmation --delete-gallery the old gallery
          will be automatically deleted if all images were moved successfully.
          For additional scripting support, this script will stop with exit code 1 whenever any error was detected.

          For all command line arguments please run python lpixmove.py move --help
    """


@cli.command()
@click.option('--old-gallery-url', required=True, help="The gallery url to move images FROM, example https://lpix.org/gallery/User+Name/12345")
@click.option('--new-gallery-url', required=True, help="The gallery url to move images TO, example https://lpix.org/gallery/User+Name/98765")
@click.option('--skip-confirmation', is_flag=True, help="If provided, the confirmation prompt will be skipped. Only recommended for use in scripts.")
@click.option('--delete-gallery', is_flag=True, help="Only has an effect if provided together with --skip-confirmation. This will automatically delete the old gallery if all images were successfully moved out of it.")
def move(old_gallery_url, new_gallery_url, skip_confirmation, delete_gallery):

    cookies = browser_cookie3.load()

    click.echo("Scanning the galleries...")

    old_page = parse_page(old_gallery_url, 'old', cookies)
    new_page = parse_page(new_gallery_url, 'new', cookies)

    images = old_page['parsed_html'].find_all(attrs={'class': 'filenametext'})
    number_of_images = len(images)

    click.echo(
        f'This will move {number_of_images} files from gallery {old_page["gallery_id"]} ( {old_page["gallery_title"]} ) to {new_page["gallery_id"]} ( {new_page["gallery_title"]} ).')

    if skip_confirmation or click.confirm('Continue?'):
        errors = False
        count = 0
        for image in images:
            image_hash = image.get('id')
            image_url = image.find(
                name='a', attrs={'class': 'gallerylink'}).get('href')

            move_url = f'https://lpix.org/ajax/gallmove.php?hash={image_hash}&gallery={new_page["gallery_id"]}'

            count += 1
            click.echo(
                f'Moving image {image_url} ({count}/{number_of_images})...')

            try:
                response = requests.get(move_url, cookies=cookies)
                if response.status_code == 200:
                    click.echo("Success!")
                else:
                    click.echo(
                        f'Something went wrong while moving image {image_url}. Got http status code {response.status_code} with message {response.text}.')
                    errors = True
            except Exception as e:
                click.echo(
                    f'Something went wrong while moving image {image_url}. Got exception {e}.')
                errors = True

        if errors:
            click.echo(
                f'Not all images moved successfully from {old_page["gallery_title"]} to {new_page["gallery_title"]}. Please fix any problems manually.')
            sys.exit(1)
        else:
            click.echo(
                f'All images moved successfully from {old_page["gallery_title"]} to {new_page["gallery_title"]}')
            if delete_gallery and skip_confirmation:
                delete_old_gallery(
                    old_page['gallery_id'], old_page['user_gallery_url'], cookies)
            elif (not skip_confirmation) and click.confirm(f'Would you like to delete the old gallery {old_page["gallery_title"]}?'):
                delete_old_gallery(
                    old_page['gallery_id'], old_page['user_gallery_url'], cookies)
            else:
                click.echo('Not deleting gallery.')
            sys.exit(0)

    else:
        click.echo("Stopping with no actions taken.")
        sys.exit(0)


if __name__ == '__main__':
    cli()
