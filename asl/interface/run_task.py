import sys
import os

if __name__ == "__main__":
    # replace current dir to asl home
    sys.path[0] = os.path.join(os.path.dirname(__file__), '..', '..')

from asl.interface.run import run_task

# Run it!
if __name__ == "__main__":
    print run_task(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
