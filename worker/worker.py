import os
from consumer import consume

if __name__ == "__main__":
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    consume(rabbitmq_host)
