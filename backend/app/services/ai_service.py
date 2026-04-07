from openai import AsyncOpenAI
from app.core.config import settings
from typing import List, Dict, Any, Optional
import json

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class AIService:
    def __init__(self):
        self.model = settings.OPENAI_MODEL

    async def generate_curriculum(
        self,
        topic: str,
        target_audience: str = "university students",
        audience_type: str = "general",
        num_lessons: int = 5,
        num_units: int = 3
    ) -> Dict[str, Any]:
        prompt = f"""Create a comprehensive curriculum for: {topic}

Target Audience: {target_audience}
Audience Type: {audience_type}
Number of Lessons: {num_lessons}
Units per Lesson: {num_units}

Generate a complete curriculum with:

1. LESSONS: Each with title, description, learning objectives
2. UNITS: Each lesson contains units with content, activities, assessments
3. THREE VERSIONS OF CONTENT:
   - Standard: Regular educational content
   - Simplified: Easier vocabulary, shorter sentences, clear structure
   - Accessibility: High contrast, screen reader friendly, no complex formatting

For SPECIAL NEEDS audience, ensure:
- Clear, simple language
- Visual aids descriptions
- Multiple ways to engage (visual, auditory, kinesthetic)
- Extended time considerations
- Alternative assessment methods

Format as JSON with this structure:
{{
  "lessons": [
    {{
      "title": "Lesson Title",
      "description": "Brief description",
      "learning_objectives": ["objective1", "objective2"],
      "duration_minutes": 45,
      "units": [
        {{
          "title": "Unit Title",
          "content": {{
            "standard": "Full content here...",
            "simplified": "Simplified version...",
            "accessibility": "Accessible version with alt text and clear structure..."
          }},
          "activities": ["activity1", "activity2"],
          "assessments": ["assessment1"]
        }}
      ]
    }}
  ]
}}

Respond ONLY with valid JSON."""

        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert instructional designer specializing in inclusive education."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return self._generate_fallback_curriculum(topic, num_lessons, num_units)

    async def generate_lesson_content(
        self,
        topic: str,
        target_audience: str,
        lesson_title: str,
        include_multimedia: bool = True,
        include_assessments: bool = True
    ) -> Dict[str, Any]:
        prompt = f"""Generate detailed lesson content for: {lesson_title}

Topic: {topic}
Target Audience: {target_audience}

Generate THREE versions of the content:

1. STANDARD VERSION:
   - Complete educational content
   - Academic vocabulary
   - Complex explanations allowed
   - Standard formatting

2. SIMPLIFIED VERSION:
   - Short sentences (max 15 words)
   - Simple vocabulary (Grade 6-8 level)
   - Bullet points for key ideas
   - Clear visual hierarchy

3. ACCESSIBILITY VERSION:
   - Screen reader optimized
   - Alt text for all images
   - High contrast structure
   - No complex tables or columns
   - Clear headings hierarchy
   - Descriptive link text

{'Include multimedia suggestions (image descriptions, video topics).' if include_multimedia else ''}
{'Include quiz questions and assessment ideas.' if include_assessments else ''}

Format as JSON:
{{
  "content_standard": {{"text": "...", "media": []}},
  "content_simplified": {{"text": "...", "key_points": []}},
  "content_accessibility": {{"text": "...", "alt_texts": [], "structure": "..."}}
}}

Respond ONLY with valid JSON."""

        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator specializing in accessibility."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=2500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return self._generate_fallback_content(lesson_title)

    async def analyze_content_quality(
        self,
        project_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        prompt = f"""Evaluate this educational content for quality.

Content Data: {json.dumps(project_data, indent=2)}

Evaluate across these dimensions (0-100):
1. INTERACTIVITY - Games, discussions, hands-on activities?
2. MULTIMEDIA - Images, videos, diagrams, audio?
3. ASSESSMENT - Quizzes, tests, practical evaluations?
4. INCLUSIVENESS - Accessibility features, special needs support?

Provide:
- Scores for each dimension
- Overall quality score
- Specific feedback
- Improvement suggestions

Format as JSON:
{{
  "interactivity_score": number,
  "multimedia_score": number,
  "assessment_score": number,
  "inclusiveness_score": number,
  "overall_score": number,
  "feedback": "detailed feedback string",
  "suggestions": ["suggestion1", "suggestion2"]
}}

Respond ONLY with valid JSON."""

        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an educational content quality evaluator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return self._generate_fallback_evaluation()

    async def smart_assist(
        self,
        text: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        prompt = f"""Analyze and improve this educational content.

Text: {text}
Context: {context or "General educational content"}

Provide suggestions in these categories:
1. SIMPLIFY - Shorter sentences, simpler words
2. INTERACTION - Add engagement opportunities
3. MEDIA - Suggest visual/audio elements
4. ACCESSIBILITY - Improve for screen readers, special needs

Format as JSON:
{{
  "suggestions": [
    {{
      "type": "simplify|interaction|media|accessibility",
      "original": "original text",
      "suggested": "improved text",
      "reason": "why this helps"
    }}
  ],
  "score": quality_score_0_to_100
}}

Respond ONLY with valid JSON."""

        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an educational content editor specializing in clarity and accessibility."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return {"suggestions": [], "score": 80}

    async def detect_alerts(
        self,
        project_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        prompt = f"""Analyze educational content for quality issues.

Project: {json.dumps(project_data, indent=2)}

Detect issues:
1. NO_INTERACTION - No engaging activities
2. NO_ASSESSMENT - No quizzes or tests
3. TEXT_TOO_LONG - Dense paragraphs over 200 words
4. NO_MEDIA - Missing visual elements
5. ACCESSIBILITY - Missing alt text, poor structure
6. COMPLEXITY - Too difficult for target audience

Return JSON array:
[{{
  "alert_type": "issue_type",
  "severity": "info|warning|error",
  "message": "human readable message",
  "suggestion": "how to fix"
}}]

Or empty array if no issues. Respond ONLY with valid JSON."""

        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI quality guardian for educational content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return []

    async def fix_content_issue(
        self,
        issue_type: str,
        content: Dict[str, Any]
    ) -> Dict[str, Any]:
        fix_prompts = {
            "no_interaction": """Add interactive activities to this content.
            Content: {content}
            Return JSON with fixed_content and explanation.""",
            
            "no_assessment": """Generate assessment questions for this content.
            Content: {content}
            Return JSON with quiz questions in fixed_content and explanation.""",
            
            "text_too_long": """Shorten this content by 40% while keeping key points.
            Content: {content}
            Return JSON with shortened content and explanation.""",
            
            "no_media": """Suggest multimedia elements for this content.
            Content: {content}
            Return JSON with media suggestions and explanation.""",
            
            "accessibility": """Improve accessibility of this content.
            Content: {content}
            Return JSON with improved content and accessibility features."""
        }
        
        prompt_template = fix_prompts.get(issue_type, fix_prompts["no_interaction"])
        prompt = prompt_template.format(content=json.dumps(content))
        
        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an educational content fixer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1500
            )
            
            content_response = response.choices[0].message.content
            return json.loads(content_response)
        except Exception as e:
            return {"fixed_content": content, "explanation": "Unable to auto-fix. Please review manually."}

    def _generate_fallback_curriculum(self, topic: str, num_lessons: int, num_units: int) -> Dict[str, Any]:
        lessons = []
        for i in range(num_lessons):
            units = []
            for j in range(num_units):
                units.append({
                    "title": f"Unit {j+1}: Core Concepts",
                    "content": {
                        "standard": f"Introduction to {topic} - Unit {j+1}. This unit covers fundamental concepts and principles.",
                        "simplified": f"{topic} basics. Unit {j+1} covers what you need to know.",
                        "accessibility": f"<h2>Unit {j+1}</h2><p>Introduction to {topic}. This section covers key ideas.</p>"
                    },
                    "activities": ["Discussion", "Practice exercise"],
                    "assessments": ["Quiz", "Group project"]
                })
            
            lessons.append({
                "title": f"Lesson {i+1}: Introduction to {topic}",
                "description": f"Foundation lesson for {topic}",
                "learning_objectives": [
                    f"Understand the basics of {topic}",
                    f"Apply {topic} concepts",
                    f"Evaluate {topic} applications"
                ],
                "duration_minutes": 45,
                "units": units
            })
        
        return {"lessons": lessons}

    def _generate_fallback_content(self, title: str) -> Dict[str, Any]:
        return {
            "content_standard": {"text": f"Content for {title}", "media": []},
            "content_simplified": {"text": f"Easy {title}", "key_points": ["Point 1", "Point 2"]},
            "content_accessibility": {"text": f"<h1>{title}</h1><p>Content here</p>", "alt_texts": [], "structure": "simple"}
        }

    def _generate_fallback_evaluation(self) -> Dict[str, Any]:
        return {
            "interactivity_score": 50,
            "multimedia_score": 50,
            "assessment_score": 50,
            "inclusiveness_score": 50,
            "overall_score": 50,
            "feedback": "Basic content structure detected. Add more interactive elements.",
            "suggestions": ["Add quizzes", "Include images", "Add discussion prompts"]
        }

ai_service = AIService()
