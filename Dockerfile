FROM ubuntu AS builder
WORKDIR /usr/src/app
COPY . .

FROM nginx:stable-alpine
COPY --from=builder /usr/src/app/public /usr/share/nginx/html
