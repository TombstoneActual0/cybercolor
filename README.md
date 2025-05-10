# Python Gradient Web Server with Custom ASCII Art

A Python script that generates a colorful gradient text, serves it via a simple HTTP server, and opens it in your browser. It supports command-line options for customization and displays a stylized ASCII art banner.

## Usage

Run the script with Python 3:

```bash
python3 your_script_name.py
Common Parameters
-h or --help: Display this help message.
-g <1|2|3|4|5|6>: Select a gradient style (1-6).
-a: Use Arial font instead of default Calibri.
You can also input custom text after starting the script, and it will apply the selected gradient.

ASCII Art Banner

╔═╗╦ ╦╔╗ ╔═╗╦═╗  ╔═╗╔═╗╦  ╔═╗╦═╗╦╔═╗╔═╗╦═╗
║  ╚╦╝╠╩╗║╣ ╠╦╝  ║  ║ ║║  ║ ║╠╦╝║╚═╗║╣ ╠╦╝
╚═╝ ╩ ╚═╝╚═╝╩╚═  ╚═╝╚═╝╩═╝╚═╝╩╚═╩╚═╝╚═╝╩╚═
              by tombstone
Required Packages
This script uses the following packages that are not included with the default Python 3 installation:

colorama
For colored terminal text output.

webbrowser
Standard library, but ensure your environment supports it.

To install colorama, run:

pip3 install colorama
Notes
The server runs temporarily, and the script automatically opens the generated HTML in your default browser.
The server will shut down after a few seconds (configurable in the script).
Make sure port 20000-20100 (or your chosen port range) is open and not blocked by your firewall.
