import sys
import time
import random
import threading
import colorama
import webbrowser
from colorama import Fore, Style
from socketserver import TCPServer
from http.server import SimpleHTTPRequestHandler

colorama.init(autoreset=True)

# Custom handler to suppress error messages
class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_request(self, code='-', size='-'):
        pass  # Do nothing

    def log_error(self, format, *args):
        pass  # Do nothing

def html_color(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def interpolate_colors(start, end, steps):
    if steps < 1:
        return [start]
    return [
        (
            int(start[0] + (end[0] - start[0]) * (i / (steps - 1))),
            int(start[1] + (end[1] - start[1]) * (i / (steps - 1))),
            int(start[2] + (end[2] - start[2]) * (i / (steps - 1)))
        ) for i in range(steps)
    ]

def get_gradient_colors(option, steps):
    if option == 1:
        segments = [
            ((255, 0, 0), (255, 102, 0)),
            ((255, 102, 0), (255, 204, 0)),
            ((230, 230, 0), (102, 255, 0)),
            ((102, 255, 0), (0, 191, 255)),
        ]
    elif option == 2:
        segments = [((128, 0, 0), (255, 0, 0))]
    elif option == 3:
        segments = [((204, 51, 0), (255, 83, 26))]
    elif option == 4:
        segments = [((26, 0, 51), (71, 0, 102))]
    elif option == 5:
        segments = [((0, 102, 102), (0, 255, 255))]
    elif option == 6:
        segments = [((0, 255, 0), (0, 204, 0))]
    else:
        return []

    all_colors = []
    for start, end in segments:
        all_colors.extend(interpolate_colors(start, end, max(1, steps // len(segments))))
    return all_colors

def apply_gradient_html(text_lines, colors):
    num_lines = len(text_lines)
    total_colors = len(colors)
    colored_text = ""

    for line_index, line in enumerate(text_lines):
        if num_lines > 1:
            color_index = int((line_index / (num_lines - 1)) * (total_colors - 1))
        else:
            color_index = 0
        r, g, b = colors[color_index]
        colored_text += f'<span style="color:{html_color(r, g, b)}">{line}</span><br/>'
        print(Fore.WHITE + Style.BRIGHT + f"\033[38;2;{r};{g};{b}m{line}\033[0m")
    return colored_text.strip()

def print_help():
    print("Usage options:")
    print("  -h, --help: Display this help message.")
    print("  -g <1|2|3|4|5|6>: Specify the gradient option directly (1-6).")
    print("  -a: Output in Arial font (default is Calibri).")
    print("Enter the text to apply the gradient after setting options, type '/d' to finish input.")

def print_ascii_art():
    ascii_art = r"""
╔═╗╦ ╦╔╗ ╔═╗╦═╗  ╔═╗╔═╗╦  ╔═╗╦═╗╦╔═╗╔═╗╦═╗
║  ╚╦╝╠╩╗║╣ ╠╦╝  ║  ║ ║║  ║ ║╠╦╝║╚═╗║╣ ╠╦╝
╚═╝ ╩ ╚═╝╚═╝╩╚═  ╚═╝╚═╝╩═╝╚═╝╩╚═╩╚═╝╚═╝╩╚═ v1
              by tombstone
    """

    gradient_option = random.randint(1, 1)
    colors = get_gradient_colors(gradient_option, 100)
    for line in ascii_art.splitlines():
        if line:
            r, g, b = random.choice(colors)
            print(Fore.WHITE + Style.BRIGHT + f"\033[38;2;{r};{g};{b}m{line}\033[0m")

def main():
    print_ascii_art()

    # Default font
    font_name = "Calibri"

    # Parse command-line arguments
    args = sys.argv[1:]
    gradient_option = None
    use_arial_font = False

    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-h", "--help"):
            print_help()
            return
        elif arg == "-g" and i + 1 < len(args):
            try:
                gradient_option = int(args[i + 1])
            except ValueError:
                print("Invalid gradient option. Must be an integer 1-6.")
                return
            i += 2
        elif arg == "-a":
            use_arial_font = True
            i += 1
        else:
            i += 1

    # Set font based on -a flag
    if use_arial_font:
        font_name = "Arial"

    # Prompt for gradient if not specified
    if gradient_option is None:
        print("Select the color gradient option:")
        print(Fore.LIGHTBLUE_EX + "1. Rainbow (ROYGB)")
        print(Fore.LIGHTRED_EX + "2. Security+ Red")
        print(Fore.LIGHTYELLOW_EX + "3. Network+ Orange")
        print(Fore.LIGHTMAGENTA_EX + "4. Tor Purple")
        print(Fore.LIGHTCYAN_EX + "5. Cloud+ Blue")
        print(Fore.LIGHTGREEN_EX + "6. Programmatic Green")
        try:
            gradient_option = int(input("Enter option number (1-6): "))
        except ValueError:
            print("Invalid input. Exiting.")
            return

    print("Enter the text to apply the gradient (type '/done' to finish input):")
    text_lines = []
    done_variations = ["/d", "/do", "/don", "/ddone", "/doone", "/donne", "/donee"]
    while True:
        line = input()
        if line.strip().lower() in done_variations:
            break
        text_lines.append(line)

    num_shades = 100
    colors = get_gradient_colors(gradient_option, num_shades)
    if not colors:
        print("Invalid gradient option selected.")
        sys.exit(1)

    result = apply_gradient_html(text_lines, colors)

    # Build HTML with the selected font
    html_output = f"""
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{
    font-family: '{font_name}', sans-serif;
  }}
</style>
</head>
<body>
{result}
</body>
</html>
"""

    # Save and serve
    with open("output.html", "w", encoding='utf-8') as f:
        f.write(html_output)

    # Start the server in a thread
    import threading

    def serve():
        print(f"Serving at port {port}")
        webbrowser.open(f"http://localhost:{port}/output.html")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            httpd.shutdown()
            httpd.server_close()

    port = random.randint(20000, 20100)
    handler = CustomHTTPRequestHandler
    httpd = TCPServer(("localhost", port), handler)

    server_thread = threading.Thread(target=serve)
    server_thread.start()

    try:
        # Keep server running for 3 seconds or until interrupted
        time.sleep(3)
    except KeyboardInterrupt:
        pass
    finally:
        httpd.shutdown()
        httpd.server_close()
        server_thread.join()

if __name__ == "__main__":
    main()
