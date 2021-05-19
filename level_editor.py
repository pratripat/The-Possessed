from LevelEditor.scripts.editor import Editor

def main():
    #Runs the editor
    editor = Editor()
    # editor.load('data/levels/trial_level.json')
    editor.main_loop()

main()
