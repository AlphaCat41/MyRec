import subprocess

def main():
    command = f"ffmpeg/bin/ffmpeg.exe -y -f gdigrab -framerate 30 -i desktop -pix_fmt yuv420p output.mp4"
   
    try:
        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error while executing ffmpeg: {e}")

if __name__== "__main__":
    main()