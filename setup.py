import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="qr_console",
    version="1.1.1",
    author="Kurush",
    author_email="ze17@ya.ru",
    description="console app builder",
    long_description_content_type="text/markdown",
    url="https://github.com/Kurush7/qr_console",
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    long_description='''
# qr_console

This project is a small console-app builder based on 
[argparse](https://docs.python.org/3/library/argparse.html) package.

### Usage example:
```python
from qr_console import QRConsole, QRCommand
console = QRConsole(hello='hello')
console.add_command(QRCommand('add', lambda a, b: print(a + b), 'sum 2 integers')
                    .add_argument('a', type=int, help='1st arg')
                    .add_argument('b', type=int, help='2nd arg'))
console.add_command(QRCommand('sub', lambda a, b: print(a - b), 'differ 2 integers')
                    .add_argument('-a', type=int, default=0, help='1st arg')
                    .add_argument('--value', '-v', type=int, help='2nd arg'))
console.add_command(QRCommand('one', lambda v, i: print(v + 1 if i else v - 1), 'change value by 1')
                    .add_argument('v', type=int)
                    .add_argument('-i', '--flag', action='store_true', help='set to inc; default is dec')
                    )
console.run()
```

### Output example:
```shell
hello
Type '-h' or '--help' to get more info
Enter commands:
?>-h
usage: PROG [-h] {add,sub,one} ...

positional arguments:
  {add,sub,one}
    add          sum 2 integers
    sub          differ 2 integers
    one          change value by 1

optional arguments:
  -h, --help     show this help message and exit
?>add -h
usage: add [-h] a b

positional arguments:
  a           1st arg
  b           2nd arg

optional arguments:
  -h, --help  show this help message and exit
?>one --help
usage: one [-h] [-i] v

positional arguments:
  v

optional arguments:
  -h, --help           show this help message and exit
  -i, --i, --flag  set to inc; default is dec
?>add 1 2
3
?>sub -a=5 -v=2
3
?>sub --value=5
-5
?>one 5
4
?>one -i 5
6
?>add
the following arguments are required: a, b
?>sub -b=5
unrecognized arguments: -b=5
?>add 1 a
argument b: invalid int value: 'a'
?>
```
'''
)
