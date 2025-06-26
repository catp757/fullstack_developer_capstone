FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1
ENV APP=/app

# Set working directory
WORKDIR $APP

# Install system dependencies
RUN apt-get update && apt-get install -y curl npm && apt-get clean

# Install Python dependencies
COPY requirements.txt $APP/
RUN pip install --no-cache-dir -r requirements.txt

# Copy full Django + React project
COPY . $APP

# Build React frontend
WORKDIR $APP/frontend
RUN npm install && npm run build

# 🟢 Ensure the build is in the correct location
# If your Django settings.py expects build files in /app/frontend/build
# this step is not necessary because we already built them in-place.
# But if you need to copy them elsewhere, you'd do it here:
# RUN cp -r build /app/djangoproj/frontend/  ← example only if needed

# Return to Django app root
WORKDIR $APP

# Ensure entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]