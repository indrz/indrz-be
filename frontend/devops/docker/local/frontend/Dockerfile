# Use Node.js LTS (Long Term Support) image
FROM node:18.20.5-alpine AS base

# Create app directory
WORKDIR /app

# Copy package files
COPY src/package*.json ./

# Install dependencies
RUN npm install
RUN npm install --save-dev @babel/plugin-proposal-private-property-in-object

# Run
FROM base

COPY --from=base /app/node_modules /app/node_modules

# Expose the development port
EXPOSE 3000

# Set host to allow external connections
ENV HOST=0.0.0.0
ENV PORT=3000
ENV NODE_OPTIONS="--openssl-legacy-provider"

# Start development server
CMD ["npm", "run", "dev"]