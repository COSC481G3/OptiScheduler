# Pull node base image
FROM node:18-alpine

# Install dependencies
WORKDIR /app/frontend
COPY ./package.json .
RUN npm install

# Move to container
COPY . .

# Set perms
RUN chown -R node /app/frontend/node_modules
USER node

# Launch app
CMD ["npm", "start"]
EXPOSE 3000
