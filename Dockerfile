FROM python:3.9-alpine AS builder
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
RUN python main.py

FROM nginx:stable-alpine
COPY --from=builder /usr/src/app/public /usr/share/nginx/html
