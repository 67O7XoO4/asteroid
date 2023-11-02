from App import App
import logging

if __name__ == "__main__" :
    
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    theApp = App()
    theApp.execute()