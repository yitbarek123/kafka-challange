FROM python:3.9

# Install dependencies
RUN pip install confluent-kafka==1.7.0

# Copy consumer code into the container
COPY consumer.py /consumer.py

# Run the consumer script
CMD ["python", "/consumer.py"]
