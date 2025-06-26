FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1

ENV APP=/app

# Set working directory
WORKDIR $APP

# Install system dependencies required for Node & Python
RUN apt-get update && \
    apt-get install -y curl npm && \
    apt-get clean

# Copy Python requirements and install them
COPY requirements.txt $APP/
RUN pip install --no-cache-dir -r requirements.txt

# Copy full source code into container
COPY . $APP

# Build frontend (React app)
WORKDIR $APP/frontend
RUN npm install && npm run build

# Go back to Django app directory
WORKDIR $APP

# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]