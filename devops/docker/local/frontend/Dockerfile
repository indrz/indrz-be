# Use Node.js LTS for Nuxt 3/Vite dev
FROM node:25.2.1-alpine AS base

WORKDIR /app

# System deps for native builds (sass, etc.)
RUN apk add --no-cache python3 make g++

# Install dependencies separately to leverage cache
COPY frontend/src/package*.json ./

RUN npm install

FROM node:25.2.1-alpine

WORKDIR /app

# System deps for native builds (sass, etc.)
RUN apk add --no-cache python3 make g++

COPY --from=base /app/node_modules ./node_modules
COPY frontend/src/ .

EXPOSE 3000

# Nuxt 3 dev server host/port
ENV HOST=0.0.0.0
ENV PORT=3000
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

CMD ["npm", "run", "dev"]
