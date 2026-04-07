"""
EduForge AI - Database Setup
Run this script after setting DATABASE_URL environment variable

Example:
Windows:
  set DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
  python setup-database.py

Linux/Mac:
  export DATABASE_URL='postgresql://postgres:password@db.xxx.supabase.co:5432/postgres'
  python setup-database.py
"""
import psycopg2
import os
import sys

def setup_database():
    conn_string = os.environ.get('DATABASE_URL', '')
    
    if not conn_string:
        print("[ERROR] DATABASE_URL not set!")
        print("\nUsage:")
        print("  Windows: set DATABASE_URL=postgresql://...")
        print("  Linux/Mac: export DATABASE_URL='postgresql://...'"
        print("\nOr run START.bat in the backend folder")
        return False
    
    # URL-encode the password if it contains special characters
    if '@' in conn_string.split('://')[1].split(':')[1].split('@')[0]:
        print("[*] Note: Password contains special characters, make sure they are URL-encoded")
    
    try:
        print("[*] Connecting to database...")
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        print("[+] Connected! Creating tables...")
        
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
        print("[+] Users table created")
        
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
        print("[+] Projects table created")
        
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
        print("[+] Lessons table created")
        
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
        print("[+] Units table created")
        
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
        print("[+] Evaluations table created")
        
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
        print("[+] Alerts table created")
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_projects_owner ON projects(owner_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_lessons_project ON lessons(project_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_units_lesson ON units(lesson_id)")
        print("[+] Indexes created")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n[SUCCESS] Database setup complete!")
        print("You can now run the EduForge AI server.")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n[DATABASE ERROR] {e}")
        print("\nTroubleshooting:")
        print("1. Check if your password is correct")
        print("2. Make sure Supabase project is active")
        print("3. Check your IP is allowed in Supabase settings")
        return False
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False

if __name__ == "__main__":
    setup_database()
    input("\nPress Enter to exit...")
