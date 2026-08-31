# Solo Grind

A gamified productivity application that transforms your real-life tasks into an RPG-style character progression system. Track your personal development, complete quests, level up skills, and watch your character grow as you accomplish your goals — with an AI mentor, Kairos, guiding you along the way.

## 🎮 Overview

Solo Grind turns daily tasks and long-term goals into an engaging game where you:
- Create quests (daily tasks, main goals, side quests, and boss challenges) with optional **recurrence schedules** — Solo Grind auto-computes difficulty and XP for you
- Break down **Boss Quests** into sub-quest objectives with AI-powered suggestions — watch the boss's HP bar deplete as you complete each objective
- Complete quests through timed **Grind** focus sessions, not a one-click button — XP is only fully awarded once you've actually put in the time
- Develop skills across six categories (Mental, Technical, Creative, Social, Business, Physical) — quests can train multiple skills at once
- Follow a Kairos-generated **Learning Path** that turns a larger goal into an editable milestone roadmap and linked quests
- Watch a real-life **Role** (Hard Coder, Athlete, Musician, Entrepreneur, and 13 others) emerge automatically from the skills you're actually building — you never pick it
- Get a curated **Daily Adventure** (3-5 quest playlist) based on your time budget and priorities — with deterministic quest selection that works without AI
- Unlock **Achievements** across 7 categories (Progression, Questing, Grind, Skills, Consistency, Exploration, Special) with Bronze to Legendary tiers, immediate celebration modals, and bonus XP
- Connect with **Friends** via unique friend codes and compete on **Leaderboards** (Weekly XP and Weekly Grind Time)
- Get proactive quest suggestions and a persistent AI chatbot from **Kairos**, your in-app mentor, grounded in your real progress
- Track your progress with an in-app **Notifications** system
- Get walked through a short onboarding loop (a seeded starter quest, a "Getting Started" checklist, and a one-time explainer) the first time you log in
- Customize your character's avatar and appearance

## 🏗️ Architecture

### Technology Stack

**Frontend:**
- Next.js 16.3.0 (React 19.2.8)
- TypeScript
- Tailwind CSS 4
- Recharts for data visualization
- Client-side routing with Next.js App Router
- Vercel Analytics

**Backend:**
- FastAPI (Python)
- MySQL database
- asyncmy for async database connections
- JWT authentication
- Google OAuth integration
- SlowAPI for rate limiting (200/minute default, 5/minute for auth endpoints)
- Groq for AI-powered features — the chat model is auto-detected from whatever's available on the configured API key (not hardcoded), with deterministic fallbacks when no key is configured

### Project Structure

```
Solo Grind/
├── nextjs-frontend/          # Next.js frontend application
│   ├── app/                  # App router pages
│   │   ├── (app)/           # Main application routes (protected)
│   │   │   ├── homepage/    # Dashboard: greeting, onboarding, suggestions, quests, skills
│   │   │   ├── character/   # Character management
│   │   │   ├── quests/      # Quest management
│   │   │   ├── skills/      # Skills overview
│   │   │   ├── grind/       # Focus timer
│   │   │   ├── adventure/   # Daily Adventure (curated quest playlist)
│   │   │   ├── paths/       # AI-assisted Learning Path roadmap
│   │   │   ├── achievements/ # Achievement tracking
│   │   │   ├── friends/      # Friend management
│   │   │   ├── leaderboards/ # Weekly leaderboards
│   │   │   ├── notifications/
│   │   │   ├── profile/     # User profile with name editing
│   │   │   └── settings/    # App settings (theme)
│   │   ├── admin/           # Admin panel routes (dashboard with analytics, users, settings, profile)
│   │   ├── page.tsx         # Login page
│   │   ├── signup/          # Registration page
│   │   ├── set-password/    # Password setup for OAuth users
│   │   └── oauth-callback/  # OAuth redirect handler
│   ├── components/          # Reusable React components (incl. KairosChat, analytics charts)
│   ├── contexts/            # React contexts (Theme)
│   └── lib/                 # Utility libraries (API, auth, etc.)
│
├── fastapi-backend/         # FastAPI backend application
│   ├── app/
│   │   ├── routers/        # API route handlers
│   │   │   ├── auth.py     # Authentication endpoints
│   │   │   ├── character.py # Character management
│   │   │   ├── quests.py   # Quest CRUD operations
│   │   │   ├── skills.py   # Skills management
│   │   │   ├── grind.py    # Focus timer sessions
│   │   │   ├── adventure.py # Daily Adventure generation & management
│   │   │   ├── paths.py     # Learning Path drafting, milestones, and quests
│   │   │   ├── kairos.py   # AI greeting + suggested tasks
│   │   │   ├── chat.py     # Persistent Kairos chatbot
│   │   │   ├── admin.py    # User management, stats, analytics (heatmap, charts)
│   │   │   ├── admin_settings.py # Admin settings (Groq API key, health checks)
│   │   │   ├── achievement.py # Achievement tracking
│   │   │   ├── social.py   # Friend management (codes, requests, friends list)
│   │   │   ├── leaderboard.py # Weekly XP and Grind Time leaderboards
│   │   │   ├── notification.py # Notification management (list, mark read, clear)
│   │   │   └── feedback.py # User feedback submission to admins
│   │   ├── core/           # Core utilities: leveling formulas, adventure engine,
│   │   │                   # skill/role matching, AI service (Groq), OAuth, JWT,
│   │   │                   # seeding, rate limiting, boss HP logic, recurrence schedules
│   │   ├── crud/           # Database CRUD operations (adventure, character, quest,
│   │   │                   # skills, user, settings, achievement, social, leaderboard,
│   │   │                   # notification)
│   │   ├── schemas/        # Pydantic request/response models
│   │   ├── services/       # External services integration
│   │   ├── utils/          # Utility functions
│   │   ├── config.py       # Configuration management
│   │   └── database.py     # Database connection pool
│   ├── main.py             # FastAPI application entry point
│   └── schema.sql          # Database schema
│
└── README.md               # This file
```

## 🎯 Core Features & Functions

### 1. Authentication System
- **Local Authentication**: Email and password-based registration and login
- **Google OAuth**: Single sign-on with Google accounts
- **JWT Tokens**: Secure session management
- **Role-based Access**: User and admin roles — admins get the full regular user experience too (see "Admin Panel" below)
- **Password Management**: Secure password hashing and validation

### 2. Character System
- **Character Creation**: One character per user, seeded automatically on first login (along with a starter quest and full skill catalog)
- **Level & XP Progression**: Gain experience points to level up
- **Power System**: Track overall character power (derived from level, total skill levels, and completed quests)
- **Rank**: A title (Unfocused → Initiate → Grinder → Disciplined → Elite → Master → Ascended) derived automatically from character level
- **Avatar Customization**:
  - Gender selection (male/female)
  - Role-based avatars with five evolving images at Role levels 1, 10, 25, 50, and 100
  - Transparent `*_nobg.png` artwork for every role, gender, and tier
  - Color themes for personalization
- **Automatic Role Detection**: Your current Role is derived live from whichever Role has accumulated the most XP — it's never manually chosen

### 3. Skills System
**Six categories, 47 built-in skills** (plus user-created custom skills): Mental, Technical, Creative, Social, Business, Physical.

Each skill tracks:
- Individual level and XP
- Progress toward next level
- Contribution to overall character power

A quest can train **up to 3 skills at once**, matched from its title/description via AI (when configured) with a deterministic keyword-matching fallback, and split with weighted XP (50% / 30% / 20% by match rank).

### 4. Quest System
Four types of quests with varying complexity:
- **Daily Quests**: Routine tasks and habits
- **Main Quests**: Major long-term goals with sub-quests
- **Side Quests**: Additional objectives
- **Boss Quests**: Major challenges with high rewards and sub-quest objectives

**Quest Recurrence System:**
Quests can be set to recur on various schedules, independent of quest type:
- **Daily**: Resets every day
- **Weekdays**: Monday through Friday only
- **Weekends**: Saturday and Sunday only
- **Times Per Week**: Complete N times within a week (e.g., 3x per week)
- **Custom Days**: Specific days of the week (e.g., Mon/Wed/Fri)
- **None**: One-time quest (default)

**Priority & Due Dates:**
- Every quest has a **Priority** (low/medium/high, defaults to medium)
- Optional **due date and time**, surfaced in quest reminders and overdue/due-today tracking

**Boss Quest Features:**
- Create sub-quests as "objectives" that chip away at the boss's HP bar
- Each objective's difficulty determines how much damage it deals (5-40 HP based on difficulty 1-5)
- Boss HP bar shows visual states: Normal → Enraged (below 50%) → Critical (below 25%) → Defeated
- AI-powered objective suggestions help break down large projects into actionable sub-quests
- Completing the final objective automatically defeats the boss and awards all XP

**Quest creation is simplified to title, description, type, optional priority, optional due date/time, and optional recurrence** — Solo Grind automatically computes:
- Difficulty (based on quest type and content length)
- XP reward
- Which skills the quest trains (up to 3, AI-matched with keyword fallback)
- Which real-life Role benefits, and by how much (derived from the matched skills' affinity to each Role)

Quests are **completed exclusively through a Grind session** — there is no instant-complete button. Status tracking: active, completed, archived. Main quests and boss quests can have sub-quests (parent-child relationships).

### 5. Grind System (Focus Timer)
- **Time-Gated Rewards**: Each quest has a minimum grind time based on its difficulty (`difficulty × 5 minutes`). Full XP is only awarded once you've met it.
- **Partial Credit**: Finishing early still awards a proportional share of the XP — quitting immediately awards none.
- **Server-Verified Duration**: Elapsed time is computed server-side from the session's start timestamp, never trusted from the client.
- **Quest Integration**: Each session is tied to a specific quest; completing the session completes the quest and distributes character/skill/Role XP together.

### 6. Daily Adventure System
**A curated, time-budgeted quest playlist for each day** — one Adventure per day, generated on demand:
- **Time Budgets**: Choose Quick (15-30 min), Standard (45-90 min), or Full (2+ hours) when generating
- **Smart Selection**: Picks 3-5 quests from your active pool using a deterministic engine that balances:
  - Main/boss quests for progress
  - Neglected skill categories for balance
  - Daily quests for maintenance
  - Side quests to fill remaining time
- **AI-Free Core**: Quest selection never depends on AI — it's pure logic based on quest types, recency, skill urgency, and time budget
- **Kairos Framing**: Optionally adds a one-line AI explanation of the day's picks (with templated fallback)
- **Flexible Management**: Replace individual quests (suggests alternatives), skip quests, or end the Adventure early
- **Adventure-Aware Grind**: Start Grind sessions directly from the Adventure page
- **One Per Day**: Can't regenerate the same day's Adventure — encourages commitment to the chosen path

### 7. Learning Paths

Learning Paths turn a broad goal into a structured roadmap that progresses through focused milestones:
- **Guided setup**: Define a goal, current experience level, weekly time budget, and optional target date.
- **AI-generated draft**: Kairos proposes a title, goal description, target skills, and editable milestones before anything is saved.
- **Explicit confirmation**: The draft stays client-side until the user reviews and confirms it.
- **Milestone quests**: The active milestone can contain linked quests and request AI-generated quest suggestions.
- **Progressive roadmap**: Completing linked quests advances milestone progress and unlocks the next stage.
- **One active Path**: A character can follow one active Learning Path at a time and may abandon it before starting another.

Learning Path drafting and quest suggestions require the Groq integration to be configured.

### 8. Role System
**17 real-life roles** (Hard Coder, Video Editor, Athlete, Musician, Entrepreneur, and more), each with a 5-tier progression title:
- **Fully Automatic**: Roles are never picked. Role XP is derived from the skills a completed quest trained, weighted by each skill's **Core** (full weight) or **Supporting** (half weight) affinity to each Role.
- **Dynamic Current Role**: Whichever Role has the highest accumulated level/XP is your current Role, computed live on every read.
- **Visual Identity**: Role-specific avatar images for each gender, plus an icon and description used throughout the UI.

### 9. Kairos — AI Mentor & Assistant
Kairos is Solo Grind's in-app mentor, backed by Groq (auto-detected chat model) when an admin has configured an API key, with graceful deterministic fallbacks otherwise — nothing ever hard-fails because AI is unavailable.
- **Personalized Greeting**: A time-aware, context-aware greeting on the homepage (AI-generated, or a curated fallback quote/status line).
- **Suggested Tasks**: A "Suggested by Kairos" homepage widget offering up to 5 new quest ideas — AI-personalized to your existing quests/skills when available, otherwise drawn from a curated pool (which occasionally mixes in one lighthearted/funny suggestion). One click adds a suggestion as a real quest.
- **Adventure Framing**: Provides a one-line explanation for Daily Adventure quest selections (AI-generated with templated fallback).
- **Persistent Chatbot**: A floating chat widget available on every page, backed by real conversation history (`chat_messages` table) and grounded in your actual character/quest/skill data — it can discuss your progress and advise you, but it's read-only: it can't create, complete, or modify anything on your behalf.

### 10. Onboarding
New characters get walked through the core loop automatically, with no separate tutorial system:
- **Starter Quest**: A single seeded quest ("Begin the Grind") created the moment your character exists, matched to skills/Role like any other quest.
- **First-Time Explainer**: Kairos's homepage greeting is replaced with a one-time explanation of how quests/grinding/skills/Roles work, until you've made real progress.
- **Getting Started Checklist**: A homepage card tracking three milestones (complete a quest, grow a skill, discover your Role), each derived live from your real data — it disappears once all three are done.

### 11. Achievement System
**30+ achievements across 7 categories**, each with tiered progression (Bronze, Silver, Gold, Platinum, Legendary):
- **Progression**: Character level milestones
- **Questing**: Quest completion counts (total, by type, boss victories)
- **Grind**: Focus session hours and streaks
- **Skills**: Skill mastery and category diversity
- **Consistency**: Daily streaks and completion patterns
- **Exploration**: Discovering features (adventures, roles, friends)
- **Special**: Hidden achievements for unique accomplishments

Achievements unlock automatically as you hit their requirements (checked after every quest completion, grind finish, and adventure end). Each achievement grants bonus XP, and achievements unlocked by finishing a Grind are returned with the completion response so the UI can celebrate immediately without another request. If one action unlocks several achievements, their celebration modals are queued and shown one at a time. Progress bars show how close you are to the next unlock.

### 12. Social Features
**Friends System:**
- Each user has a unique, randomly-generated **Friend Code** (8 characters, no confusing letters)
- No user directory or search — codes are the only way to connect (privacy-first design)
- Send friend requests by entering someone's code
- Accept/decline incoming requests
- View friends list with their current level, role, rank, and avatar
- View a friend's character, skill progress, and achievement progress
- See whether friends are currently online based on recent authenticated activity
- Remove friends or block users as needed — blocked users are tracked separately from the friends list

**Leaderboards:**
Two weekly leaderboards, scoped to you and your accepted friends only:
- **Weekly XP**: Total character XP earned this week (Monday-Sunday)
- **Weekly Grind Time**: Total grind session time this week
- Shows rank, character name, level, current role, and metric value
- Resets every Monday
- Only includes accepted friends (not pending requests)

### 13. Notifications System
In-app notification system tracking important events:
- **Server-Side Notifications**: Friend requests (incoming and accepted), achievement unlocks, admin feedback responses
- **Client-Side Notifications**: Quest reminders (due dates, recurring quests ready to reset), daily adventure availability, grind session reminders
- **Browser Notifications**: Optional browser notifications for grind reminders and break timers (user must enable from notifications page)
- **Live Toasts & Sounds**: Newly arriving reminders and server events appear as in-app toasts; social events use a distinct sound, while achievement and rank celebrations use a celebration chime
- Unread count badge in sidebar navigation (server notifications only)
- Filter by all/unread, mark individual notifications or the full feed as read, and clear local reminders without deleting server-side history
- **Feedback System**: Users can submit feedback directly to admins through the notifications page, creating an admin notification for every admin except the sender

### 14. Admin Panel
Admins get the full regular user experience *and* an admin interface — logging in takes you to the normal homepage, with an **"Admin Panel"** link in the profile menu, and a **"Back to User Page"** button in the admin sidebar to switch back.
- **Dashboard**: System statistics with real-time health monitoring and comprehensive analytics
  - GitHub-style activity heatmap showing 365 days of grind session activity
  - User growth line chart tracking daily signups over 30 days
  - Quest trends bar chart comparing creation vs completion rates
- **User Management**: List, search, activate/deactivate, change roles, delete users
- **Admin Notifications**: A dedicated `/admin/notifications` route keeps admins inside the admin layout while showing the same account-level notification feed and unread badge
- **AI Integration Settings**: Configure/remove the Groq API key, test the AI connection — this key gates every AI-powered feature app-wide

## 🔄 Key Processes & Workflows

### User Registration & Onboarding
1. User signs up with email/password or Google OAuth
2. System creates user account
3. On first data access, a character is automatically created, backfilled with the full skill catalog, and seeded with a starter quest
4. OAuth users are prompted to set a password
5. Every user — including admins — lands on the regular homepage after login

### Quest Completion Flow
1. User creates a quest with just a title, description, and type
2. Solo Grind computes difficulty, XP reward, matched skills (up to 3), and Role linkage automatically
3. User starts a Grind session on the quest
4. Timer runs while the user works; the minimum time for full XP is shown up front
5. User finishes the session — server computes actual elapsed time
6. System awards, proportional to time spent:
   - Character XP
   - Skill XP (to each matched skill)
   - Role XP (to the derived Role, if any)
7. Character, skills, and the Role level up if thresholds are met
8. Quest status updates to "completed"
9. Newly unlocked achievements are returned with the Grind result and displayed one at a time after any higher-priority boss-defeat or level-up celebration

### Leveling System
**Character Leveling:**
- XP required = `level * 100`

**Skill Leveling:**
- XP required = `level * 50`
- Each skill levels independently; contributes to overall character power

**Role Leveling:**
- XP required = `75 + (level - 1) * 30`
- XP accumulates per Role, derived from skill-affinity-weighted quest rewards
- Current Role is automatically whichever Role has the highest level/XP
- Role titles progress across 5 tiers as you level up

### Focus Session (Grind) Process
1. User picks an active quest to grind (from Quests, the homepage, or the Grind picker)
2. Timer starts and counts up; the full-reward threshold is shown
3. User works on the task
4. User clicks "Finish" — server computes elapsed time and the XP multiplier
5. Quest completes, XP/skill/Role rewards are awarded and displayed
6. User returned to the picker with updated stats

### Avatar Customization Process
1. User navigates to character page
2. Opens avatar picker
3. Selects gender, Role (affects avatar image), and color theme
4. Preview updates in real-time
5. User saves changes; avatar displayed across the application

## 📊 Database Schema

### Core Tables
- **users**: User accounts and authentication
- **characters**: One character per user with level/XP/power
- **skills**: Skill catalog (6 categories, 47 built-ins, plus user-created)
- **character_skills**: Per-character skill progression
- **roles**: Real-life Role catalog with progression titles and images
- **character_role_xp**: Per-character Role progression
- **role_skill_affinity**: Which skills feed which Role's XP, and how strongly (core/supporting)
- **quests**: Quest management with parent-child relationships, Role linkage, and recurrence schedules
- **quest_skill_rewards**: Per-skill XP rewards for a quest (a quest can train multiple skills)
- **quest_completions**: Completion log for recurring quests (for streaks and recurrence tracking)
- **grind_sessions**: Focus timer session tracking
- **adventures**: Daily Adventure records (one per character per day)
- **adventure_quests**: Quest picks within an Adventure with status tracking (pending/completed/skipped)
- **paths**: Active, completed, or abandoned Learning Paths for a character
- **path_milestones**: Ordered milestone roadmap and progress for each Learning Path
- **achievements**: Achievement catalog with categories, tiers, and requirements
- **character_achievements**: Unlocked achievements per character
- **user_relationships**: Friend requests, friendships, and blocks
- **notifications**: Server-side notifications (friend requests, achievements, admin feedback)
- **xp_events**: XP gain ledger for leaderboards and analytics
- **chat_messages**: Persisted Kairos chatbot conversation history, per user
- **app_settings**: App-wide config (e.g. the Groq API key)

### Key Relationships
- User (1) → (1) Character
- User (1) → (Many) User Relationships (friends, blocks)
- Character (1) → (Many) Character Skills
- Character (1) → (Many) Character Role XP
- Character (1) → (Many) Character Achievements
- Character (1) → (Many) Quests
- Character (1) → (Many) Adventures
- Character (1) → (Many) Learning Paths
- Learning Path (1) → (Many) Path Milestones
- Path Milestone (1) → (Many) Quests
- Quest (1) → (Many) Quest Skill Rewards
- Quest (1) → (Many) Quest Completions (recurring quests only)
- Quest (1) → (Many) Grind Sessions
- Quest (1) → (Many) Sub-quests (boss/main quests)
- Adventure (1) → (Many) Adventure Quests
- Role (1) → (Many) Role Skill Affinities
- User (1) → (Many) Chat Messages
- User (1) → (Many) XP Events

## 🚀 Getting Started

### Prerequisites
- Node.js 20+ and npm/yarn/pnpm
- Python 3.10+
- MySQL 8.0+
- (Optional) A [Groq](https://console.groq.com) API key to enable AI-powered features

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd fastapi-backend
   ```

2. **Install Python dependencies:**
   ```bash
   python -m pip install fastapi "uvicorn[standard]" asyncmy pydantic-settings \
     PyJWT "passlib[bcrypt]" authlib slowapi httpx email-validator \
     python-multipart itsdangerous
   ```

   > The backend currently does not include a pinned Python dependency manifest. The command above installs the packages imported by the application; add a lock file before using reproducible production builds.

3. **Configure environment variables:**
   Create `.env.local` file with:
   ```env
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=your_user
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=solo_grind
   JWT_SECRET=your_jwt_secret_key
   
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
   FRONTEND_URL=http://localhost:3000
   
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=admin_password
   ```

4. **Initialize database:**
   ```bash
   mysql -u your_user -p < schema.sql
   ```

5. **Run the backend server:**
   ```bash
   python main.py
   # or
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

6. **(Optional) Enable AI features:** log in as the admin account, go to Admin Panel → Settings, and add a Groq API key. Without one, Kairos and quest skill-matching fall back to deterministic logic automatically.

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd nextjs-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Configure environment variables:**
   Create `.env.local` file with:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

   The application will be available at `http://localhost:3000`

### Default Admin Account
On first startup, an admin account is automatically created using the credentials from `ADMIN_EMAIL` and `ADMIN_PASSWORD` environment variables. Admins can use the app as a normal user (homepage, quests, grind, etc.) and reach the Admin Panel via a link in the profile menu.

## 🔌 API Endpoints

### Authentication (`/auth`)
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login with credentials
- `GET /auth/google/login` - Initiate Google OAuth flow
- `GET /auth/google/callback` - Google OAuth callback
- `GET /auth/me` - Get current user info (email, role, profile picture, full name)
- `POST /auth/me/picture` - Upload profile picture
- `DELETE /auth/me/picture` - Remove profile picture
- `PATCH /auth/me/name` - Update user's full name
- `POST /auth/set-password` - Set password for OAuth users

### Character (`/character`)
- `GET /character/me` - Get user's character
- `PATCH /character/me` - Update character name
- `PATCH /character/me/avatar` - Update character avatar
- `GET /character/me/activity-heatmap` - Get the current user's activity heatmap
- `GET /character/me/skill-balance` - Get the current user's skill-category balance
- `GET /character/{user_id}` - Get a friend's character profile
- `GET /character/avatar-roles` - Get available avatar roles

### Skills (`/skills`)
- `GET /skills` - Get skill catalog
- `POST /skills` - Create custom skill
- `GET /skills/me` - Get character's skill progression
- `GET /skills/{user_id}` - Get a friend's skill progression

### Quests (`/quests`)
- `POST /quests` - Create new quest (title, description, type, optional recurrence only — everything else is computed)
- `GET /quests` - List quests (with filters)
- `GET /quests/{quest_id}` - Get single quest
- `GET /quests/{quest_id}/boss` - Get boss quest HP view with objectives
- `GET /quests/{quest_id}/boss/suggestions` - Get AI-powered boss objective suggestions
- `POST /quests/{quest_id}/complete` - Complete a quest directly (not used by the UI, which always routes through Grind)
- `PATCH /quests/{quest_id}` - Update quest details
- `DELETE /quests/{quest_id}` - Delete a quest

### Grind (`/grind`)
- `POST /grind/start` - Start focus session
- `POST /grind/{session_id}/pause` - Pause an active focus session
- `POST /grind/{session_id}/resume` - Resume a paused focus session
- `POST /grind/{session_id}/finish` - Finish focus session, awarding time-gated XP and returning any achievements unlocked by that completion

### Adventure (`/adventure`)
- `GET /adventure/today` - Get or check for today's Daily Adventure
- `POST /adventure/generate` - Generate a new Daily Adventure with time budget (quick/standard/full)
- `POST /adventure/{adventure_id}/quests/{quest_id}/replace` - Swap out a quest in the Adventure
- `POST /adventure/{adventure_id}/quests/{quest_id}/skip` - Skip a quest in the Adventure
- `POST /adventure/{adventure_id}/end` - Manually end the Adventure early

### Learning Paths (`/paths`)
- `POST /paths/draft` - Generate an editable Learning Path draft without saving it
- `POST /paths/confirm` - Confirm a reviewed draft and create its milestone roadmap
- `GET /paths/active` - Get the character's active Learning Path
- `GET /paths/{path_id}` - Get an owned Learning Path
- `POST /paths/{path_id}/abandon` - Abandon an active Learning Path
- `GET /paths/{path_id}/milestones/{milestone_id}/quests` - List quests linked to a milestone
- `GET /paths/{path_id}/milestones/{milestone_id}/quest-suggestions` - Generate quest suggestions for a milestone

### Kairos (`/kairos`)
- `GET /kairos/greeting` - Personalized greeting (AI or fallback)
- `GET /kairos/suggestions` - Suggested starter quests (AI-personalized or curated fallback)

### Chat (`/chat`)
- `GET /chat/history` - Get persisted chatbot conversation
- `POST /chat/message` - Send a message, get a context-grounded reply
- `DELETE /chat/history` - Clear conversation history

### Achievements (`/achievements`)
- `GET /achievements/me` - Get character's achievement progress with unlock status
- `GET /achievements/{user_id}` - Get a friend's achievement progress

### Friends (`/friends`)
- `GET /friends` - Get friend code, friends list, incoming/outgoing requests
- `POST /friends/request` - Send friend request using a friend code
- `POST /friends/{user_id}/accept` - Accept incoming friend request
- `DELETE /friends/{user_id}` - Remove a friend
- `POST /friends/{user_id}/block` - Block a user
- `DELETE /friends/{user_id}/block` - Unblock a user

### Leaderboards (`/leaderboards`)
- `GET /leaderboards/{type}` - Get weekly leaderboard (weekly_xp or weekly_grind_time)

### Notifications (`/notifications`)
- `GET /notifications` - Get user's notifications with unread count
- `POST /notifications/{notification_id}/read` - Mark notification as read
- `POST /notifications/read-all` - Mark all notifications as read

### Feedback (`/feedback`)
- `POST /feedback` - Submit feedback (creates notifications for admins other than the sender)

### Admin (`/admin`)
- `GET /admin/users` - List/search users with pagination
- `PATCH /admin/users/{user_id}/status` - Activate/deactivate a user
- `PATCH /admin/users/{user_id}/role` - Change a user's role
- `DELETE /admin/users/{user_id}` - Delete a user
- `GET /admin/stats` - System-wide statistics (users, characters, quests, sessions)
- `GET /admin/activity-heatmap` - 365 days of grind session activity data
- `GET /admin/user-growth` - 30-day user signup trend data
- `GET /admin/quest-trends` - 30-day quest creation and completion data

### Admin Settings (`/admin/settings`)
- `GET /admin/settings` - Get current settings (keys masked)
- `POST /admin/settings/groq-api-key` / `DELETE /admin/settings/groq-api-key` - Manage the Groq API key
- `POST /admin/settings/test-ai` - Test the AI connection
- `GET /admin/settings/health` - Backend/database/AI health check

## 🎨 Frontend Features

### Theme System
- Light and dark mode support
- Persistent theme preference
- Smooth transitions between themes

### Responsive Design
- Mobile-friendly interface
- Adaptive layouts for different screen sizes
- Fixed sidebars with independently scrolling content, on both the user and admin shells

### Components
- **AppSidebar** / **AdminSidebar**: Main navigation for app and admin routes, each with a fixed (non-scrolling) shell
- **SidebarProfileMenu**: Profile dropdown — includes the Admin Panel link for admins
- **KairosMessage**: Kairos greeting/explainer message bubble
- **KairosChat**: Floating persistent AI chatbot, available on every authenticated page
- **ProfileCard**: User profile management with avatar upload and full name editing
- **AvatarPicker**: Interactive avatar customization
- **CreateQuestPanel**: Quest creation form (title, description, type, priority, due date/time, recurrence)
- **QuestCard**: Individual quest display with inline editing of priority, due date, and recurrence
- **BossCard**: Boss quest HP bar with objective management and AI suggestions
- **BossDefeatedModal**: Celebration modal when a boss quest is completed
- **XpBar**: Progress bar for XP visualization
- **LevelUpModal**: Level-up celebration modal
- **AchievementUnlockedModal**: Queued achievement celebration showing tier and bonus XP immediately after a Grind
- **SessionExpiredModal**: Handles expired JWT tokens (8-hour expiry) with automatic logout
- **NotificationsPanel**: Shared user/admin notification feed with all/unread filters, feedback submission, read controls, and browser-notification setup
- **NotificationToast**: Polls for newly arriving local and server notifications and displays event-specific in-app toasts and sounds
- **ProtectedLink**: Client-side navigation wrapper with auth protection
- **AppearanceToggle**: Dark/light mode switcher
- **ActivityHeatmap**: GitHub-style contribution squares (365 days of grind sessions)
- **UserGrowthChart**: Line chart showing 30-day user signup trends
- **QuestTrendsChart**: Bar chart comparing quest creation vs completion
- **CharacterHero** / **CharacterStats** / **CharacterMilestones** / **CharacterRoleCard**: Character page sections — avatar/name/XP header, power/rank/streak/achievement stat tiles, next-milestone callouts, and current Role progress
- **AchievementShowcase** / **AchievementCard** / **AchievementOverview**: Featured recently-unlocked achievements, individual achievement tiles by tier, and category-level unlock progress
- **CreateSkillForm** / **SkillProgressCard**: Custom skill creation and per-skill progress display with sorting/filtering
- **ConnectFriendCard** / **FriendCard**: Friend-code entry/incoming-request card and individual friend display with level, role, rank, and avatar

## 🔐 Security Features

- JWT token-based authentication with 8-hour token expiry
- Automatic token refresh on page visibility change (prevents mid-session expiration on mobile)
- Secure password hashing (bcrypt)
- Rate limiting with SlowAPI (200/minute default, 5/minute for auth endpoints)
- CORS configuration for API protection
- Session middleware for secure state management (also used for the Google OAuth CSRF `state`)
- Input validation with Pydantic models
- SQL injection prevention with parameterized queries
- File upload validation (size and type restrictions)

## 📝 Development Notes

### Backend Structure
- **Routers**: Define API endpoints and request handlers
- **CRUD**: Database operations isolated from business logic
- **Core**: Leveling formulas, adventure engine, boss HP logic, recurrence schedules, skill/Role matching (AI + keyword fallback), the AI service wrapper, OAuth/JWT, rate limiting, seeding
- **Schemas**: Request/response validation with Pydantic

### Frontend Structure
- **App Router**: File-based routing with Next.js App Router
- **Client Components**: Interactive components with "use client" directive
- **API Layer**: Centralized API calls in `/lib/api.ts`
- **Auth Management**: Token handling in `/lib/auth.ts`
- **Type Safety**: Full TypeScript coverage

### Code Conventions
- Python: PEP 8 style guide, async/await pattern
- TypeScript: Strict mode, functional components with hooks
- CSS: Tailwind utility classes, mobile-first approach

### AI Design Philosophy
Every AI-powered feature (skill matching, greetings, suggestions, boss objective suggestions, adventure framing, chat) has a deterministic fallback and is designed to never hard-fail the surrounding feature if Groq is unavailable, slow, or unconfigured — the app is fully usable with zero AI configuration. The Daily Adventure's core quest selection is entirely deterministic and AI-free.

## 🚧 Future Enhancements

Potential features for future development:
- Quest templates and sharing
- Mobile app version
- Push notifications and email notifications (in-app notifications exist)
- Custom rewards system
- Integration with calendar apps
- Agentic Kairos (letting the chatbot take actions, not just advise)
- Team/guild features for collaborative quests
- Quest marketplace for sharing community-created quests

## 📄 License

This project is private and proprietary.

## 🤝 Contributing

This is a private project. Contact the project owner for contribution guidelines.

---

**Solo Grind** - Level up your life, one quest at a time! 🎮✨
