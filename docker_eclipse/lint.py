import os
import sys

def run_docker_lint(args):
    os.system("docker exec nvidia_docker /usr/local/bin/pylint {}".format(' '.join(args)))

if __name__ == '__main__':
    run_docker_lint(sys.argv[1:])
    
