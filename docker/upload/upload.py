
import argparse
import os
import subprocess
import tarfile
import easywebdav
import posixpath
import json
from urlparse import urlparse


def zip_results(output_file, source_dir, input_json):
    with tarfile.open(output_file, 'w:gz') as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
        tar.add(input_json, arcname=os.path.basename(input_json))


def upload(filename, url, user, password):
    o = urlparse(url)
    client = easywebdav.connect(
                 host=o.netloc,
                 protocol=o.scheme,
                 username=user,
                 password=password,
             )
    remote_path = posixpath.join(o.path + filename)
    client.upload(filename, remote_path)

    remote_url = posixpath.join(url, filename)
    output = { 'url': remote_url }
    print json.dumps(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--json_input",
                        help="The filename (including path, full or relative) "
                             "of the json file that specifies the input to the "
                             "classifier.",
                        type=str)
    parser.add_argument("--filename",
                        type=str)
    parser.add_argument("--input_directory",
                        help="Folder (including path, full or relative) "
                             "in which houses the original images Sherlock workflow",
                        required=True, type=str)
    parser.add_argument("--webdav-user", type=str, required=True)
    parser.add_argument("--webdav-password", type=str, required=True)
    parser.add_argument("--webdav-url", type=str, required=True)

    args = parser.parse_args()

    zip_results(args.filename, args.input_directory, args.json_input)

    upload(args.filename, args.webdav_url, args.webdav_user, args.webdav_password)

