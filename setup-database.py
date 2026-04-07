"""
EduForge AI - Database Setup Script
Run this to create all tables in Supabase
"""
import psycopg2
import os

def setup_database():
    # Get connection string from environment or ask user
    conn_string = os.environ.get('DATABASE_URL')
    
    if not conn_string:
        print("❌ DATABASE_URL not set!")
        print("\nPlease set your Supabase connection string:")
        print("  export DATABASE_URL='postgresql://postgres:[PASSWORD]@db.jnzqdznnhcjeovmvznuq.supabase.co:5432/postgres'")
        return False
    
    try:
        print(f"🔄 Connecting to database...")
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        print("✅ Connected! Creating tables...")
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                username VARCHAR(100) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                full_name VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        print("✓ Users table created")
        
        # Projects table
        cursor.execute("""
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
            )
        """)
        print("✓ Projects table created")
        
        # Lessons table
        cursor.execute("""
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
            )
        """)
        print("✓ Lessons table created")
        
        # Units table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS units (
                id SERIAL PRIMARY KEY,
                lesson_id INTEGER REFERENCES lessons(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                content JSONB DEFAULT '{}',
                order_index INTEGER DEFAULT 0,
                activities JSONB DEFAULT '[]',
                assessments JSONB DEFAULT '[]',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        print("✓ Units table created")
        
        # Evaluations table
        cursor.execute("""
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
            )
        """)
        print("✓ Evaluations table created")
        
        # Alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
                alert_type VARCHAR(50) NOT NULL,
                severity VARCHAR(20) DEFAULT 'warning',
                message TEXT NOT NULL,
                suggestion TEXT,
                is_resolved BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        print("✓ Alerts table created")
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_projects_owner ON projects(owner_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_lessons_project ON lessons(project_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_units_lesson ON units(lesson_id)")
        print("✓ Indexes created")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n🎉 Database setup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Correct DATABASE_URL")
        print("2. Correct password in the connection string")
        return False

if __name__ == "__main__":
    setup_database()
