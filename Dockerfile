# Pull node base image
FROM node:18-alpine

# Install dependencies
RUN apk add --no-cache python3 py3-pip

WORKDIR /app/frontend
COPY /frontend/package.json .
RUN npm install

WORKDIR /app/backend
COPY /backend/requirements.txt .
RUN pip install -r requirements.txt

# Move to container
WORKDIR /app
COPY . .

WORKDIR /app/frontend
RUN npm run build

# Launch app
WORKDIR /app/backend
#CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
CMD ["python3", "base.py"]
EXPOSE 5000