# Frontend - Next.js React Application

This is the frontend application for the Academic Assignment Helper & Plagiarism Detector, built with Next.js 16, React 19, TypeScript, and Tailwind CSS.

## Features

- ✅ **Modern React Architecture** - Component-based, reusable, maintainable
- ✅ **TypeScript** - Type-safe development
- ✅ **Tailwind CSS** - Utility-first styling matching Figma design
- ✅ **Next.js App Router** - Modern routing and layouts
- ✅ **Figma Design Integration** - All assets from Figma Desktop MCP server

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Figma Desktop app running (for image assets)

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js app router pages
│   ├── login/             # Login page
│   ├── signup/            # Signup page
│   ├── dashboard/         # Dashboard pages
│   │   ├── analysis/     # Assignment Analysis
│   │   ├── sources/       # Source Search
│   │   └── history/       # Previous Queries
│   └── layout.tsx         # Root layout
├── components/            # Reusable React components
│   ├── Sidebar.tsx        # Navigation sidebar
│   ├── Header.tsx         # Page header
│   └── UploadArea.tsx    # File upload component
└── public/                # Static assets
```

## API Integration

The frontend communicates with the FastAPI backend through:
- API routes proxied via Next.js rewrites (`/api/*` → `http://localhost:8000/*`)
- Authentication via JWT tokens stored in localStorage

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Design System

All design tokens match the Figma Final Design:
- Colors: `#f9f9fb` (background), `#1d4ed8` (primary), `#e8edfb` (active states)
- Typography: Inter font family
- Spacing: 8px, 12px, 16px, 32px grid
- Components: Matching Figma specifications exactly

## Deployment

The frontend can be deployed to:
- **Vercel** (recommended for Next.js)
- **Railway**
- **Docker** (with custom Dockerfile)

See deployment configuration in `docker-compose.yml` for containerized setup.
