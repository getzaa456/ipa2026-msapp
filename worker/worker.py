import os
from consumer import consume

if __name__ == '__main__':
    # อ่านค่า host ของ RabbitMQ จาก Environment Variable (default เป็น rabbitmq)
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    consume(rabbitmq_host)
