# Guest Relations Frontend

A modern React frontend for the Guest Relations system, built with Vite and Tailwind CSS.

## Architecture

```
frontend/
├── src/
│   ├── App.jsx                 # Main application component with routing
│   ├── main.jsx                # Application entry point
│   ├── index.css               # Global styles and Tailwind imports
│   ├── components/             # Reusable UI components
│   │   ├── Navigation.jsx      # Main navigation bar
│   │   ├── AuthModal.jsx       # Authentication modal
│   │   ├── CasesTable.jsx      # Cases data table
│   │   ├── UploadModal.jsx     # Document upload workflow
│   │   └── upload/             # Upload workflow components
│   │       ├── UploadStep.jsx  # File upload step
│   │       ├── EditStep.jsx    # Case editing step
│   │       ├── ReviewStep.jsx  # Review step
│   │       ├── ConfirmStep.jsx # Confirmation step
│   │       ├── StepHeader.jsx  # Step header component
│   │       ├── ProgressBar.jsx # Progress indicator
│   │       └── Navigation.jsx  # Step navigation
│   ├── pages/                  # Page components
│   │   ├── CasesPage.jsx       # Cases management page
│   │   └── FollowupsPage.jsx   # Followups management page
│   └── services/               # API service layer
│       └── api.js              # API client functions
├── public/                     # Static assets
├── package.json                # Dependencies and scripts
├── vite.config.js             # Vite configuration
├── tailwind.config.js         # Tailwind CSS configuration
└── postcss.config.js          # PostCSS configuration
```

## Core Features

- **Document Processing**: Multi-step upload workflow with AI integration
- **Case Management**: Comprehensive data tables with CRUD operations
- **Followup Management**: Track case followups and status
- **Authentication**: JWT-based user authentication with role-based access
- **Responsive Design**: Mobile-first responsive interface

## Technology Stack

- **Framework**: React 18 with Hooks
- **Build Tool**: Vite for fast development and building
- **Styling**: Tailwind CSS for utility-first styling
- **Routing**: React Router for client-side navigation
- **HTTP Client**: Fetch API for backend communication

## Quick Start

### Prerequisites
- Node.js 16+

### Installation
```bash
npm install

# Copy environment template
cp env.example .env
# Edit .env with your API URL

# Run development server
npm run dev
```

## Environment Variables

Copy `env.example` to `.env` and configure:

```env
VITE_API_URL=http://localhost:8000/api
VITE_ENVIRONMENT=development
```

## Development

- Hot reload enabled for fast development
- ESLint configured for code quality
- Tailwind CSS for styling
- Responsive design for all devices
