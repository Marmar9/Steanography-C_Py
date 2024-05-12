# Helo in kool aplikejszon

## App setup

- Python setup 3.12 needed
```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ deactivate
```

- Build stuff
```bash
$ mkdir bin
$ make
```

- Add bin to pythonpath 
```bash
$ export PYTHONPATH="$PWD/bin"
```

- Generate .pyi types (needed only for development)
```bash
$ ./gen-pyright-types.sh
```
