# EduForge AI

AI-Powered Educational Content Platform with Multi-Version Support

## Features

- **Smart Curriculum Generation**: Create complete lessons, units, and full curriculum plans
- **Multi-Version Content**: Automatically generate Standard, Simplified, and Accessibility versions
- **Smart Assist**: Real-time AI suggestions for content improvement
- **Smart Alerts**: AI Quality Guardian detects issues in real-time
- **Fix with AI**: One-click auto-fix for detected issues
- **Live Quality Meter**: Track Interactivity, Multimedia, Assessment, and Inclusiveness
- **Inclusive Education**: Built-in support for students with special needs

## Architecture

- **Backend**: Python FastAPI
- **Database**: SQLite (initial) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Real-time**: WebSockets
- **AI**: OpenAI API integration

## Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

### 3. Run the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open Browser

Navigate to: http://localhost:8000

## Project Structure

```
EduForge-AI/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # AI & WebSocket services
│   ├── static/
│   │   ├── css/          # Styles
│   │   └── js/           # Frontend JavaScript
│   ├── templates/        # HTML templates
│   └── main.py           # Application entry point
├── .env.example
└── requirements.txt
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/token` - Login
- `GET /api/v1/auth/me` - Get current user

### Projects
- `POST /api/v1/projects/` - Create project
- `GET /api/v1/projects/` - List projects
- `GET /api/v1/projects/{id}` - Get project
- `DELETE /api/v1/projects/{id}` - Delete project
- `POST /api/v1/projects/generate-curriculum` - Generate full curriculum

### AI Features
- `POST /api/v1/ai/smart-assist` - Analyze and improve content
- `POST /api/v1/ai/generate-content` - Generate lesson content
- `POST /api/v1/ai/evaluate/{project_id}` - Evaluate project quality
- `POST /api/v1/ai/analyze/{project_id}` - Detect issues
- `POST /api/v1/ai/fix-alert/{alert_id}` - Fix detected issue
- `GET /api/v1/ai/quality-metrics/{project_id}` - Get quality scores

### WebSocket
- `WS /ws/{project_id}?token={jwt}` - Real-time updates

## Database Schema

### Users
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| email | String | Unique email |
| username | String | Unique username |
| hashed_password | String | Bcrypt hash |
| full_name | String | Display name |

### Projects
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| title | String | Project title |
| topic | String | Educational topic |
| target_audience | String | Target audience |
| audience_type | String | general/special_needs/mixed |
| status | String | draft/generated/completed |

### Lessons
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| project_id | Integer | Foreign key to Project |
| title | String | Lesson title |
| content_standard | JSON | Standard version content |
| content_simplified | JSON | Simplified version |
| content_accessibility | JSON | Accessibility version |
| learning_objectives | JSON | List of objectives |

### Units
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| lesson_id | Integer | Foreign key to Lesson |
| title | String | Unit title |
| content | JSON | Multi-version content |
| activities | JSON | Learning activities |
| assessments | JSON | Assessment methods |

### Evaluations
| Field | Type | Description |
|-------|------|-------------|
| interactivity_score | Float | 0-100 score |
| multimedia_score | Float | 0-100 score |
| assessment_score | Float | 0-100 score |
| inclusiveness_score | Float | 0-100 score |
| overall_score | Float | Weighted average |

## Multi-Version Content

The system automatically generates three versions of content:

1. **Standard Version**: Regular educational content with full vocabulary
2. **Simplified Version**: 
   - Short sentences (max 15 words)
   - Grade 6-8 vocabulary level
   - Clear bullet points
3. **Accessibility Version**:
   - Screen reader optimized
   - Alt text for images
   - High contrast structure
   - Descriptive headings

## AI Prompts

### Curriculum Generation
Generates complete curriculum with lessons, units, activities, and assessments. Supports inclusive education with adaptations for special needs learners.

### Content Quality Analysis
Evaluates content across four dimensions:
- Interactivity (engagement opportunities)
- Multimedia (visual/audio elements)
- Assessment (quizzes and evaluations)
- Inclusiveness (accessibility features)

### Smart Assist
Provides suggestions for:
- Simplifying text
- Adding interaction
- Including media
- Improving accessibility

## Environment Variables

```
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4-turbo-preview
SECRET_KEY=your-secret-key
```

## License

MIT License
