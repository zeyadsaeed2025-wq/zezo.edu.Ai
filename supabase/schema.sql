-- EduForge AI - Supabase Database Setup
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    topic VARCHAR(255),
    target_audience VARCHAR(100),
    audience_type VARCHAR(50) DEFAULT 'general',
    owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Lessons table
CREATE TABLE IF NOT EXISTS lessons (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER DEFAULT 0,
    learning_objectives JSONB DEFAULT '[]',
    content_standard JSONB DEFAULT '{}',
    content_simplified JSONB DEFAULT '{}',
    content_accessibility JSONB DEFAULT '{}',
    duration_minutes INTEGER DEFAULT 30,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Units table
CREATE TABLE IF NOT EXISTS units (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content JSONB DEFAULT '{}',
    order_index INTEGER DEFAULT 0,
    activities JSONB DEFAULT '[]',
    assessments JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Evaluations table
CREATE TABLE IF NOT EXISTS evaluations (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    interactivity_score FLOAT DEFAULT 0,
    multimedia_score FLOAT DEFAULT 0,
    assessment_score FLOAT DEFAULT 0,
    inclusiveness_score FLOAT DEFAULT 0,
    overall_score FLOAT DEFAULT 0,
    feedback TEXT,
    suggestions JSONB DEFAULT '[]',
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) DEFAULT 'warning',
    message TEXT NOT NULL,
    suggestion TEXT,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_projects_owner ON projects(owner_id);
CREATE INDEX IF NOT EXISTS idx_lessons_project ON lessons(project_id);
CREATE INDEX IF NOT EXISTS idx_units_lesson ON units(lesson_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_project ON evaluations(project_id);
CREATE INDEX IF NOT EXISTS idx_alerts_project ON alerts(project_id);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;
ALTER TABLE units ENABLE ROW LEVEL SECURITY;
ALTER TABLE evaluations ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own data" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own data" ON users FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own projects" ON projects FOR SELECT USING (auth.uid() = owner_id);
CREATE POLICY "Users can insert own projects" ON projects FOR INSERT WITH CHECK (auth.uid() = owner_id);
CREATE POLICY "Users can update own projects" ON projects FOR UPDATE USING (auth.uid() = owner_id);
CREATE POLICY "Users can delete own projects" ON projects FOR DELETE USING (auth.uid() = owner_id);

-- For development: Allow all operations (remove in production!)
CREATE POLICY "Allow all on users" ON users FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on projects" ON projects FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on lessons" ON lessons FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on units" ON units FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on evaluations" ON evaluations FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on alerts" ON alerts FOR ALL USING (true) WITH CHECK (true);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for projects
CREATE TRIGGER update_projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE users IS 'User accounts for EduForge AI';
COMMENT ON TABLE projects IS 'Educational content projects';
COMMENT ON TABLE lessons IS 'Individual lessons within projects';
COMMENT ON TABLE units IS 'Units within lessons containing actual content';
COMMENT ON TABLE evaluations IS 'Quality evaluations for projects';
COMMENT ON TABLE alerts IS 'Quality alerts and warnings';
