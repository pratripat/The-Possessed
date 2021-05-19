from scripts.editor import Editor

def main():
    #Runs the editor
    editor = Editor()
    editor.load('data/saved.json')
    editor.main_loop()

main()
