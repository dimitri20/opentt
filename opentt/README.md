# OpenTT - Open-Source Timetable Management System

OpenTT is a complete, production-ready timetable management system for schools and universities. It uses Google OR-Tools CP-SAT constraint solver to automatically generate conflict-free schedules based on institutional constraints.

## Features

- **Automated Scheduling**: Uses CP-SAT constraint solver to generate optimal timetables
- **Flexible Constraints**: Support for 17+ constraint types (availability, preferences, capacity, etc.)
- **Multi-view Timetables**: View schedules by class, teacher, or room
- **Real-time Progress**: Track solver progress with live updates
- **Export Options**: Export timetables to HTML and CSV
- **Full CRUD Interface**: Manage all resources through intuitive web interface
- **Production-Ready**: Docker Compose setup with all services

## Technology Stack

### Backend
- **Python 3.12** with FastAPI
- **SQLAlchemy 2.0** with PostgreSQL 16
- **Google OR-Tools** CP-SAT solver
- **Celery** for async task processing
- **Redis** for task queue and pub/sub

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development
- **TanStack Query** for server state management
- **shadcn/ui** components with Tailwind CSS
- **React Router v6** for navigation

## Quick Start

### Prerequisites

- Docker and Docker Compose
- (Optional) Node.js 18+ and Python 3.12+ for local development

### Running with Docker Compose

```bash
cd opentt
docker compose up --build
```

Access the application:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up database (requires PostgreSQL running)
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost/opentt"
alembic upgrade head

# Run API server
uvicorn app.main:app --reload

# Run Celery worker (in separate terminal)
celery -A app.celery_app.celery_app worker --loglevel=info
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
opentt/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # FastAPI route handlers
│   │   ├── core/            # Configuration and settings
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic layer
│   │   └── solver/          # OR-Tools CP-SAT solver
│   ├── tests/               # Backend tests
│   ├── alembic/             # Database migrations
│   ├── main.py              # FastAPI application
│   └── celery_app.py        # Celery configuration
├── frontend/
│   └── src/
│       ├── components/      # React components
│       ├── pages/           # Page components
│       ├── lib/             # Utilities
│       └── api/             # API client
├── docker-compose.yml       # Docker Compose configuration
└── README.md
```

## Data Model

The system manages the following entities:

- **Institutions**: Top-level organization
- **Days & Periods**: Time structure
- **Buildings & Rooms**: Physical resources with capacity
- **Teachers**: Staff with availability constraints
- **Subjects**: Courses/classes
- **Students**: Organized in Years → Groups → Subgroups hierarchy
- **Activities**: Teaching sessions linking subjects, teachers, and groups
- **Constraints**: Rules and preferences (17+ types)
- **Solve Jobs**: Solver executions with solutions

## Usage

### 1. Institution Setup

1. Create a new institution
2. Define days of week (e.g., Monday-Friday)
3. Define periods (e.g., 8:00-9:00, 9:00-10:00, etc.)
4. Add buildings and rooms with capacities

### 2. Resource Management

1. Add teachers with email and availability
2. Add subjects
3. Create student hierarchy:
   - Year (e.g., Year 10)
   - Groups within year (e.g., Class A, Class B)
   - Subgroups within groups (e.g., Language groups)

### 3. Activity Creation

Create activities specifying:
- Subject
- Assigned teachers
- Assigned groups/subgroups
- Duration (number of periods)
- Split count (how many times per week)
- Preferred rooms

### 4. Constraint Configuration

Add constraints such as:
- Teacher not available (hard constraint)
- Teacher max hours per day (soft constraint)
- Students max hours per day (soft constraint)
- Room not available (hard constraint)
- Activity preferred starting time (soft constraint)
- And 12+ more constraint types

### 5. Solve

1. Navigate to Solve page
2. Set time limit (default: 300 seconds)
3. Click "Solve" to start the solver
4. Monitor real-time progress:
   - Solutions found
   - Current objective value
   - Time elapsed
5. View generated timetable on completion

### 6. View Timetables

Multiple views available:
- **By Class**: See schedule for each student group
- **By Teacher**: See schedule for each teacher
- **By Room**: See room utilization

Each view displays a grid with:
- Days as columns
- Periods as rows
- Activity details in each cell

### 7. Export

Export timetables to:
- **HTML**: Formatted tables for printing/sharing
- **CSV**: Structured data for further processing

## Constraint Types

### Hard Constraints (Must be satisfied)
- No teacher conflicts (same teacher, different activities, same time)
- No student group conflicts
- No room conflicts
- Teacher availability
- Room availability
- Room capacity

### Soft Constraints (Penalties)
- Teacher max hours per day
- Students max hours per day
- Teacher max gaps per day
- Students max gaps per day
- Activity preferred starting time
- Activity preferred starting day
- Activities not on same day
- Activities consecutive
- Activities same starting time
- Activities same starting day
- Room preference
- And more...

## Testing

### Backend Tests

```bash
cd backend
docker compose exec api pytest tests/ -v --cov=app
```

### Frontend E2E Tests

```bash
cd frontend
npm run test:e2e
```

## API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

### Request Flow

1. User creates/updates resources via React frontend
2. Frontend makes API calls to FastAPI backend
3. Backend stores data in PostgreSQL
4. User triggers solve via UI
5. Backend enqueues Celery job
6. Worker picks up job and runs OR-Tools solver
7. Solver publishes progress updates to Redis
8. Frontend polls job status and displays progress
9. On completion, solution stored in database
10. Frontend fetches and displays timetable

### Solver Algorithm

The CP-SAT solver:
1. Loads all activities, constraints, and resources
2. Creates boolean variables for each possible assignment
   - `x[activity, day, period, room]`
3. Adds hard constraints (conflicts, availability)
4. Adds soft constraints with penalty weights
5. Minimizes total penalty
6. Returns optimal or best-effort solution

## Performance

Typical solve times:
- **Small** (3 teachers, 10 activities): < 30 seconds
- **Medium** (20 teachers, 100 activities): < 5 minutes
- **Large** (50+ teachers, 300+ activities): May timeout, returns best found

Optimization tips:
- Use multi-threading (`num_search_workers`)
- Set reasonable time limits
- Minimize soft constraint penalties
- Reduce problem size if possible

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/opentt/issues)
- Documentation: See inline code comments and API docs

## Acknowledgments

- Google OR-Tools for the constraint solver
- FastAPI for the excellent web framework
- shadcn/ui for beautiful UI components
- React and Vite for frontend tooling
