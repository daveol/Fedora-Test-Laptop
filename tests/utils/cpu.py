import multiprocessing
import subprocess


def create_cpu_load(sleep=30):
    """
    create some artificial cpu load to heat stuff up
    """

    procs = []

    # Create cpu load
    for core in range(multiprocessing.cpu_count()):
        procs.append(subprocess.Popen(['sha256sum','/dev/random']))

    # Give some heat-up time
    time.sleep(sleep)

    # clean the processes
    for proc in procs:
        proc.kill()
