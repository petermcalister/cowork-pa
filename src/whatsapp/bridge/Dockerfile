# Multi-stage build for the WhatsApp Go bridge
# Stage 1: Build with CGO enabled (required by go-sqlite3)
FROM golang:1.25-alpine AS builder

RUN apk add --no-cache gcc musl-dev

WORKDIR /app
COPY go.mod go.sum main.go ./
RUN go get go.mau.fi/whatsmeow@latest && go mod tidy
RUN CGO_ENABLED=1 go build -o whatsapp-bridge .

# Stage 2: Minimal runtime image
FROM alpine:3.21

RUN apk add --no-cache ca-certificates

WORKDIR /app
COPY --from=builder /app/whatsapp-bridge .

EXPOSE 8080

# store/ is mounted as a volume for persistent session + message data
VOLUME ["/app/store"]

ENTRYPOINT ["./whatsapp-bridge"]
