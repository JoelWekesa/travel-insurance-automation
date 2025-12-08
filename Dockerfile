FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright dependencies as root (requires system packages)
RUN playwright install-deps chromium

# Create non-root user
RUN useradd -m -u 1000 appuser

# Switch to non-root user to install Playwright browsers
USER appuser

# Install Playwright browsers as appuser (browsers go to user's home directory)
RUN playwright install chromium

# Switch back to root to copy files and set permissions
USER root

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p screenshots logs

# Change ownership of app directory
RUN chown -R appuser:appuser /app

# Switch to non-root user for runtime
USER appuser

# Run the scheduler
CMD ["python", "scheduler.py"]