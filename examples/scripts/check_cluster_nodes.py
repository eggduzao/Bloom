import os
import subprocess
import psutil

def system_summary():
    print(f"CPU cores: {os.cpu_count()}")
    mem = psutil.virtual_memory()
    print(f"Total Memory: {mem.total / (1024**3):.2f} GB")

def can_download():
    try:
        subprocess.check_call(['wget', '-q', '--spider', 'http://google.com'])
        print("Internet connection available: YES")
    except subprocess.CalledProcessError:
        print("Internet connection available: NO")

def fastq_dump_available():
    try:
        subprocess.check_call('fastq-dump --stdout SRR000001 --maxSpotId 1 > /dev/null', shell=True)
        print("fastq-dump functional: YES")
    except subprocess.CalledProcessError:
        print("fastq-dump functional: NO")

def current_active_workers():
    """
    Print the current number of active processes consuming CPU resources.
    """
    active_processes = len([p for p in psutil.process_iter(['cpu_percent']) if p.info['cpu_percent'] > 0])
    print(f"Active CPU-consuming processes: {active_processes}")

if __name__ == "__main__":
    system_summary()
    can_download()
    fastq_dump_available()
    current_active_workers()

