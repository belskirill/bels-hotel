FROM python:3.13


WORKDIR /app


RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"



COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt


COPY . .

CMD alembic upgrade head; python src/main.py