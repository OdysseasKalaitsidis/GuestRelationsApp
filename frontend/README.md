# Guest Relations Frontend

A modern, responsive React frontend for the Guest Relations system, built with Vite and Tailwind CSS.

## Architecture Overview

The frontend follows a clean, component-based architecture:

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
│   │   ├── FollowupsPage.jsx   # Followups management page
│   │   └── TasksPage.jsx       # Tasks management page
│   └── services/               # API service layer
│       └── api.js              # API client functions
├── public/                     # Static assets
├── package.json                # Dependencies and scripts
├── vite.config.js             # Vite configuration
├── tailwind.config.js         # Tailwind CSS configuration
└── postcss.config.js          # PostCSS configuration
```

## Core Features

### 1. Document Processing Workflow
- **Multi-step Upload**: Guided workflow for document processing
- **File Validation**: Support for PDF and DOCX formats
- **AI Integration**: Automated case extraction and feedback generation
- **Case Management**: Edit and review extracted cases before creation

### 2. Case Management
- **Data Table**: Comprehensive cases display with sorting and filtering
- **CRUD Operations**: Create, read, update, and delete cases
- **Bulk Operations**: Handle multiple cases efficiently
- **User Assignment**: Assign cases to team members

### 3. Followup Management
- **Followup Tracking**: Monitor case followups and status
- **AI Suggestions**: AI-powered followup recommendations
- **Status Management**: Track followup progress and completion

### 4. Task Management
- **Task Creation**: Create and assign tasks to team members
- **Priority Management**: Set task priorities and deadlines
- **Progress Tracking**: Monitor task completion status

### 5. Authentication & Security
- **JWT Authentication**: Secure user authentication
- **Role-based Access**: Admin and user role management
- **Session Management**: Secure session handling

## Technology Stack

- **Framework**: React 18 with Hooks
- **Build Tool**: Vite for fast development and building
- **Styling**: Tailwind CSS for utility-first styling
- **Routing**: React Router for client-side navigation
- **State Management**: React Hooks for local state
- **HTTP Client**: Fetch API for backend communication

## Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn package manager

### Installation
```bash
cd frontend
npm install
```

### Environment Setup
Create a `.env` file with:
```env
VITE_API_URL=http://localhost:8000/api
```

### Development
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Building for Production
```bash
npm run build
```

The built application will be in the `dist/` directory.

## Component Architecture

### Core Components

#### Navigation
- Main navigation bar with routing
- User authentication status
- Responsive mobile menu

#### UploadModal
- Multi-step document processing workflow
- File upload and validation
- AI-powered case extraction
- Case editing and review
- Bulk case creation

#### Data Tables
- Sortable and filterable data display
- Pagination for large datasets
- Responsive design for mobile devices

### Page Components

#### CasesPage
- Display all cases in a data table
- Case creation and editing
- Bulk operations
- Search and filtering

#### FollowupsPage
- Followup management interface
- Status tracking and updates
- AI suggestion integration

#### TasksPage
- Task creation and management
- Priority and deadline handling
- User assignment

## API Integration

The frontend communicates with the backend through the `api.js` service layer:

- **Authentication**: Login, logout, user management
- **Documents**: Upload, process, workflow automation
- **Cases**: CRUD operations, bulk creation
- **Followups**: Creation and management
- **Tasks**: Task operations and assignment

## State Management

The application uses React Hooks for state management:

- **Local State**: Component-level state with `useState`
- **Effect Management**: Side effects with `useEffect`
- **Context**: Authentication state sharing
- **Props**: Component communication

## Styling & Design

### Tailwind CSS
- Utility-first CSS framework
- Responsive design system
- Custom component styling
- Dark/light theme support

### Design Principles
- **Clean Interface**: Minimal, focused design
- **Responsive Layout**: Mobile-first approach
- **Accessibility**: WCAG compliance
- **Performance**: Optimized rendering and loading

## Development Guidelines

### Code Quality
- **ESLint**: Code linting and formatting
- **Component Structure**: Consistent component organization
- **Naming Conventions**: Clear, descriptive names
- **Error Handling**: Comprehensive error boundaries

### Performance
- **Code Splitting**: Route-based code splitting
- **Lazy Loading**: Component lazy loading
- **Optimization**: Bundle size optimization
- **Caching**: API response caching

### Testing
- **Unit Tests**: Component testing
- **Integration Tests**: API integration testing
- **E2E Tests**: User workflow testing

## Deployment

### Railway Deployment
The frontend is configured for Railway deployment:
- Environment-based configuration
- Build optimization
- Static asset serving

### Build Optimization
- Tree shaking for unused code
- Asset compression and optimization
- CDN integration for static assets

## Contributing

1. Follow the existing component structure
2. Use consistent naming conventions
3. Add comprehensive tests
4. Update documentation
5. Ensure responsive design
6. Test across different devices

## License

This project is licensed under the MIT License.
