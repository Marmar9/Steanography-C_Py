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
- Web app
```bash
$ python api.py
```
- Client example
```bash
$ python wav.py -e chime_big_ben.wav .\1200px-Sunflower_from_Silesia2-min.jpg result
$ python wav.py -d result.wav decoded
```

## References

- https://www.youtube.com/watch?v=M9ZwuIv3xz8
