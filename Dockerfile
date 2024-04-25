# Multistage build for efficiency
FROM python:3.11 AS builder

# Set working directory in the container
WORKDIR /web

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Copy and install requirements
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Second stage of the build
FROM builder AS final

# Set working directory in the container
WORKDIR /web

ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv
# Copy the Django project files
COPY . .

# Expose port for Django application
EXPOSE 8000

# Command to run Django development server
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]