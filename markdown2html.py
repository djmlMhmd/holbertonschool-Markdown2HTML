#!/usr/bin/python3
"""
This is a module that converts a Markdown file to HTML.
"""

import sys
import os
import markdown

"""
Converts Markdown
"""
def markdown2html():
    """
    Converts a Markdown file to HTML.

    This function checks if the number of arguments is less than 3 and if
    the Markdown file exists. If either of these conditions is not met, it
    prints an error message to STDERR and exits with status code 1.
    Otherwise, it reads the Markdown file, converts the content to HTML,
    writes the result to the HTML file, and exits with status code 0.
    """
    # Check if we have 3 arguments
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # check if the file exists
    if not os.path.exists(markdown_file):
        print("Error: Missing " + markdown_file, file=sys.stderr)
        sys.exit(1)

    # Read the file and parse it
    with open(markdown_file, 'r') as f:
        lines = f.read()
        html = markdown.markdown(lines)

        # Write the html file
        with open(html_file, 'w') as f:
            f.write(html)

    """If the Markdown file exists and is successfully converted to HTML,
    do nothing and exit with status code 0"""
    sys.exit(0)


if __name__ == "__main__":
    markdown2html()