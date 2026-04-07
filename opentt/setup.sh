#!/bin/bash

echo "🚀 OpenTT Setup Script"
echo "======================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Copy .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
else
    echo "ℹ️  .env file already exists"
fi

echo ""
echo "🐳 Starting Docker services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for database to be ready..."
sleep 10

echo ""
echo "🗄️  Running database migrations..."
docker-compose exec -T backend alembic upgrade head

echo ""
echo "✅ Setup complete!"
echo ""
echo "📍 Access points:"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs:    http://localhost:8000/api/docs"
echo "   - Frontend:    http://localhost:5173"
echo ""
echo "📋 Useful commands:"
echo "   - View logs:       docker-compose logs -f"
echo "   - Stop services:   docker-compose down"
echo "   - Restart:         docker-compose restart"
echo ""
echo "🎉 Happy scheduling!"
