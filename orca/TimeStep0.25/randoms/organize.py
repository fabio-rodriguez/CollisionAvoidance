import os
import shutil

if __name__=="__main__":

    cwd = os.getcwd()

    for dir in os.listdir():
        try:
            vals = dir.split("Dron")
            num = vals[0].split("Exp")[-1]
            if not os.path.isdir(f"{cwd}/{num}"): 
                os.mkdir(f"{cwd}/{num}")
        except:
            pass

        try:
            shutil.copy(f"{cwd}/{dir}", f"{cwd}/{num}/{dir}")
            os.remove(f"{cwd}/{dir}")
        except:
            pass

        