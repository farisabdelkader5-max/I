# ContentForge AI — Product Blueprint v1

## Product definition

ContentForge AI is an AI content research and video production platform for English faceless creators.

It turns a niche or goal into multiple ready-to-produce content systems:

- Viral Shorts System
- Documentary System
- Repurpose Pack
- Trend Hunter System

## Target users

Initial target:
- English faceless YouTube Shorts/TikTok/Reels creators.
- Creators in curiosity, science, history, AI, business, cars/F1, and strange facts.

Later:
- Agencies.
- E-commerce brands.
- Educators.
- Newsletter/media teams.

## First MVP workflow

1. User enters niche, platform, goal, style, duration.
2. Research Agent generates content questions and angles.
3. Idea Scoring Agent ranks ideas.
4. System Agent produces multiple content systems.
5. Script Agent creates script and storyboard.
6. Stock Agent searches Pexels/Pixabay/paid providers.
7. Voice Agent creates voiceover.
8. Render Agent creates final video using Shotstack/Creatomate/Remotion.
9. Learning Agent records approvals, ratings, and performance.

## Production architecture

Frontend:
- Next.js dashboard

Backend:
- FastAPI or NestJS

Database:
- Postgres/Supabase

Queue:
- Redis + BullMQ/Celery

Storage:
- Cloudflare R2 or S3

Providers:
- AI writer: OpenAI/Gemini/Claude
- Search: OpenAI web search/Tavily/SerpAPI/YouTube API
- Stock: Pexels, Pixabay, Storyblocks, Shutterstock
- Voice: ElevenLabs or equivalent TTS provider
- Render: Shotstack, Creatomate, or Remotion
- Optional AI video: Runway, Veo, Kling, Luma

## Learning system

The platform should learn through:

- User ratings
- User edits
- Accepted/rejected ideas
- Stock assets selected vs rejected
- Render completion rate
- Cost per successful video
- Later: imported publishing performance such as retention, CTR, likes, saves

It should improve:

- Idea ranking
- Hook templates
- Script structures
- Stock keyword generation
- Visual selection
- Provider routing
- User-specific style memory

It must not:

- Rewrite its own code without review
- Publish without permission
- Scrape copyrighted videos
- Clone voices or faces without consent
- Hide provider/license requirements

## MVP feature list

Must-have:
- Campaign generator
- Multiple content systems
- Idea scoring
- Video plan generation
- Stock search adapter
- Render JSON preview
- Feedback learning loop

Next:
- Auth
- Projects
- Credits
- Payments
- Real video rendering
- Real voiceover storage
- Admin dashboard

Later:
- Team workspace
- Brand kits
- Direct publishing
- Analytics import
- Fine-tuned ranking model
- Template marketplace

## Pricing idea

Free:
- 3 generated plans, watermark or no export

Starter:
- $9-15/month
- Short-form plans and limited renders

Pro:
- $29-49/month
- More renders, HD export, brand kit, repurpose packs

Agency:
- $99+/month
- Team, high limits, API, white-label templates
