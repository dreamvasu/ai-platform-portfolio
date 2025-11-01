# Frontend Pages Design

## 1. Home / Landing Page

**Purpose:** Hook them in 3 seconds

**Sections:**
```jsx
<Hero>
  - Headline: "From 65% Match to 90% Match in 12 Hours"
  - Subheadline: "How I transformed into an AI Platform Engineer"
  - CTA: [View Journey] [Live Demos] [GitHub]
  - Animated background with tech stack icons
</Hero>

<StatsSection>
  - Technologies Mastered: 8
  - Hours Invested: 12
  - GitHub Commits: 50+
  - Live Deployments: 3
</StatsSection>

<JourneyPreview>
  - Timeline visualization (animated)
  - Before/After skills comparison
  - Key achievements
</JourneyPreview>

<TechStackShowcase>
  - Interactive tech stack grid
  - Hover for details
  - Links to deep dive pages
</TechStackShowcase>

<LiveDemosSection>
  - Embedded RAG chatbot
  - K8s deployment screenshots
  - GCP Cloud Run metrics
  - Interactive architecture diagram
</LiveDemosSection>

<CTASection>
  - "Ready to see how I did it?"
  - Link to full journey
</CTASection>
```

## 2. Journey Page

**Purpose:** Tell the complete story

**Layout:**
```jsx
<TimelineView>
  Hour 0: The Challenge
  - Job requirements analysis
  - Gap identification
  - Decision to sprint

  Hour 1-2: Kubernetes Fundamentals
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways

  Hour 3-4: GCP Cloud Run
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways

  Hour 5-6: Infrastructure as Code
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways

  Hour 7-8: RAG System
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways

  Hour 9-10: Integration & Testing
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways

  Hour 11-12: Deployment & Documentation
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways
</TimelineView>

<SkillsEvolution>
  - Before sprint skills matrix
  - After sprint skills matrix
  - Visual comparison
</SkillsEvolution>

<GitHubActivity>
  - Commit history visualization
  - Code snippets
  - Links to repos
</GitHubActivity>
```

## 3. Technical Deep Dive Pages

### A. Kubernetes Deep Dive
```jsx
<Overview>
  - What is Kubernetes
  - Why it matters for AI/ML platforms
  - My learning approach
</Overview>

<Implementation>
  - Architecture diagram
  - Code snippets (YAML files)
  - Deployment process
  - Troubleshooting stories
</Implementation>

<Results>
  - Screenshots of running cluster
  - kubectl commands used
  - Performance metrics
  - Lessons learned
</Results>

<Resources>
  - Links to docs I used
  - GitHub repo link
  - Commands cheat sheet
</Resources>
```

### B. GCP Deep Dive
```jsx
<Overview>
  - GCP services used (Cloud Run, Vertex AI)
  - Architecture decisions
  - Cost considerations
</Overview>

<Implementation>
  - Step-by-step deployment guide
  - gcloud commands used
  - Configuration screenshots
  - Integration with Vertex AI
</Implementation>

<Results>
  - Live deployment URL
  - Performance metrics
  - Auto-scaling demos
  - Cost analysis
</Results>
```

### C. RAG System Deep Dive
```jsx
<Overview>
  - RAG architecture
  - Tech stack (ChromaDB, OpenAI)
  - Use case for portfolio
</Overview>

<Implementation>
  - Vector database setup
  - Embedding generation
  - Query flow
  - Code walkthrough
</Implementation>

<Demo>
  - Live chatbot embedded
  - Example queries
  - Response quality showcase
</Demo>

<Technical>
  - API endpoints
  - Request/response format
  - Performance optimization
</Technical>
```

### D. Terraform / IaC Deep Dive
```jsx
<Overview>
  - Infrastructure as Code principles
  - Why Terraform
  - Resources managed
</Overview>

<Implementation>
  - Terraform code walkthrough
  - GCP resources provisioned
  - State management
  - Modules used
</Implementation>

<Results>
  - Infrastructure diagram
  - terraform plan output
  - Cost estimation
  - Reproducibility demo
</Results>
```

## 4. About Page

**Purpose:** Professional profile + personal story

```jsx
<Introduction>
  - Photo
  - Elevator pitch
  - Current role & experience
</Introduction>

<Background>
  - 10 years software architecture
  - Key achievements
  - Industries worked in
  - Technologies mastered
</Background>

<WhyThisRole>
  - Career transition story
  - Why AI/ML platform engineering
  - What excites you
  - What you bring
</WhyThisRole>

<Resume>
  - Download button
  - Key highlights
  - Work history timeline
</Resume>

<Contact>
  - LinkedIn
  - GitHub
  - Email
  - Portfolio chatbot CTA
</Contact>
```

## 5. Blog / Learning Log

**Purpose:** Show thought process and learning journey

**Posts structure:**
- "Hour 1-2: Breaking into Kubernetes"
- "Hour 3-4: GCP Cloud Run - First Impressions"
- "Hour 5-6: Infrastructure as Code Mindset Shift"
- "Hour 7-8: Building a Production-Ready RAG System"
- "Hour 9-10: The Integration Hell and How I Survived"
- "Hour 11-12: Shipping to Production"
- "Lessons Learned: What I'd Do Differently"
- "From Application Dev to Platform Engineer"
