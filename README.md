pyinstaller.exe --onefile --noconsole .\octgnify.py


docker build --network=host -f docker/Dockerfile -t octgnify .

