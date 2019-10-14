import sys
import subprocess

usage = \
"""$ python publish.py LAMBDA_MODULE.py

Publish a python3.7 module containing a lambda function to aws.
Asuumes `aws configure` has been performed.
"""

def main(module: str, fname: str):
    subprocess.run([
        "aws",
        "lambda",
        "update-function-code",
        "--function-name",
        fname,
        "--zip-file",
        module
    ])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(usage)
    module = "fileb://" + sys.argv[1]
    fname = sys.argv[2]
    main(module, fname)
