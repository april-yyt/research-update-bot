FROM python:3.10-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install as package (requires setup.py)
RUN pip install --no-cache-dir -e .

# Create a volume for the database
VOLUME /app/data

# Set the database path to the volume location
ENV DB_PATH=/app/data/research_bot.db

CMD ["python", "-m", "main"]