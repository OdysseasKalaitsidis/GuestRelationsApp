# Guest Relations Frontend

A modern React application for managing guest relations cases, PDF uploads, and AI-powered followup tracking.

## Features

- **PDF Upload & Processing**: Upload PDFs and automatically extract case data
- **AI Feedback Generation**: Get AI-powered suggestions for followup actions
- **Case Management**: View and manage all cases with their details
- **Followup Tracking**: Manage followup tasks with status updates and assignments
- **Complete Workflow**: End-to-end processing from PDF to database
- **Modern UI**: Clean, responsive interface built with Tailwind CSS

## Pages

### 1. Upload Page (`/upload`)
- Dedicated PDF upload interface
- Complete workflow execution
- Real-time progress tracking
- Success summary with statistics

### 2. Cases Page (`/cases`)
- View all cases with their details
- Expandable rows showing associated followups
- Refresh data from backend
- Upload new PDFs via modal

### 3. Followups Page (`/followups`)
- Manage all followup tasks
- Edit followup details inline
- Update status and assignments
- Delete followups

## Technology Stack

- **React 18** - Modern React with hooks
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool and dev server

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

## API Integration

The frontend integrates with the backend API endpoints:

- **PDF Upload**: `/pdf/upload`
- **AI Feedback**: `/ai/feedback`
- **Complete Workflow**: `/workflow/complete`
- **Cases**: `/cases/*`
- **Followups**: `/followups/*`

## Usage

### 1. Upload a PDF
1. Navigate to the Upload page
2. Select a PDF file
3. Click "Start Complete Workflow"
4. Monitor the progress through each step
5. View the final results and statistics

### 2. View Cases
1. Go to the Cases page
2. See all cases in a table format
3. Click "Show Details" to expand and view followups
4. Use the refresh button to get latest data

### 3. Manage Followups
1. Navigate to the Followups page
2. Edit followup details inline
3. Update status and assignments
4. Delete followups as needed

## File Structure

```
src/
├── components/          # Reusable UI components
│   ├── CasesTable.jsx  # Cases display table
│   └── UploadModal.jsx # PDF upload modal
├── pages/              # Page components
│   ├── CasesPage.jsx   # Cases management page
│   ├── FollowupsPage.jsx # Followups management page
│   └── UploadPage.jsx  # PDF upload page
├── services/           # API service functions
│   └── api.js         # All API calls
├── App.jsx            # Main app component
└── main.jsx           # App entry point
```

## Development

### Adding New Features
1. Create new components in `src/components/`
2. Add new pages in `src/pages/`
3. Update API functions in `src/services/api.js`
4. Add routes in `src/App.jsx`

### Styling
- Uses Tailwind CSS utility classes
- Custom components follow the existing design patterns
- Responsive design for mobile and desktop

### State Management
- Uses React hooks for local state
- API calls are centralized in service functions
- Error handling and loading states included

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Ensure backend is running on port 8000
   - Check CORS settings in backend
   - Verify API endpoints are correct

2. **PDF Upload Issues**
   - Ensure file is a valid PDF
   - Check file size limits
   - Verify backend PDF processing is working

3. **Data Not Loading**
   - Check browser console for errors
   - Verify database connection
   - Check API response format

## Contributing

1. Follow the existing code structure
2. Use consistent naming conventions
3. Include error handling
4. Test with different data scenarios
5. Ensure responsive design

## License

This project is part of the Guest Relations Management System.
