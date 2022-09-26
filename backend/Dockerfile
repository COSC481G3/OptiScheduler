# Pull python base image
FROM python:latest

# Install dependencies
WORKDIR /app/backend
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Move to container
COPY . .

# Launch app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000