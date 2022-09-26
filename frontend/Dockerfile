# Pull node base image
FROM node:18-alpine

# Install dependencies
WORKDIR /app/frontend
COPY ./package.json .
RUN npm install

# Move to container
COPY . .

# Launch app
CMD ["npm", "start"]
EXPOSE 3000