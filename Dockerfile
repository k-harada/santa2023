FROM python:3.10

WORKDIR /workspace

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY puzzle.py puzzle.py
COPY rubik24 rubik24
COPY rubik48 rubik48
COPY rubik72 rubik72
COPY magic612 magic612
COPY magic622 magic622
COPY input input
COPY rubiks-cube-NxNxN-solver rubiks-cube-NxNxN-solver
COPY rubik_large rubik_large
COPY tasks.py tasks.py

ENTRYPOINT ["inv"]
CMD ["--list"]
