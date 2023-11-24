FROM node:18.12.1-alpine as build

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN npm install

RUN npm install --save-dev @babel/plugin-proposal-private-property-in-object

# Set the NODE_OPTIONS environment variable
ENV NODE_OPTIONS="--openssl-legacy-provider"

# Copy the entire app directory to the container
COPY . .

# Generate the Nuxt.js static files
# RUN npm version patch --git-tag-version false && npx nuxt generate

EXPOSE 3000

CMD ["npm", "run", "dev"]
