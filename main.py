# With this main.py, I'm going to import 'website' package. And grap the create_app() -> to create app and run
from website import create_app

app = create_app()

# <In order to run flask>
if __name__ == '__main__':  # explain: only if we run this file, not if we import this file which is 'main.py', 
    app.run(debug=True) # Then we're going to run this line.
                        # If you import main.py from another file and you didn't this line, it would run webserver.
                        # debug=True: everytime we change any of python code, it's going to automatically rerun the websever.