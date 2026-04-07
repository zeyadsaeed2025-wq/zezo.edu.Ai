#!/bin/bash
# EduForge AI - Auto Deploy Script

echo "🎓 EduForge AI Deployment"
echo "========================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Deploying to Render.com...${NC}"

# Create Render Blueprint
cat > render.yaml << 'EOF'
services:
  - type: web
    name: eduforge-ai
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    autoDeploy: true
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
EOF

echo -e "${GREEN}✓ Created render.yaml${NC}"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://render.com/blueprints"
echo "2. Click 'New Blueprint Instance'"
echo "3. Connect your GitHub repo"
echo "4. Set OPENAI_API_KEY environment variable"
echo "5. Click 'Apply'"
echo ""
echo "🌐 Your app will be live at: https://eduforge-ai.onrender.com"
