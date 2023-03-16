from textify import load_server, load_cleaner

if __name__ == "__main__":
    cleaner = load_cleaner()
    server = load_server(cleaner)
    server.serve()
