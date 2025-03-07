# main.py
import subprocess

def main():
    # Run Hlv.py
    subprocess.run(["python", "Hlv.py"])
    
    # Run Texture.py
    subprocess.run(["python", "Texture.py"])

if __name__ == "__main__":
    main()
