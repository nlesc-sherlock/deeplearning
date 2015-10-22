
#!/usr/bin/env python
"""Analyze an image using a trained deep learning network and return tags found
of found concepts in the image.
Usage:
  generatetags.py <imagepath>
"""

from taggeneration import generate_tags
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print generate_tags(args['<imagepath>'])
