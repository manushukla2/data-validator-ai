# 📊 AI Data Validator - Pension Fund Edition

A sophisticated AI-powered data validation system specifically designed for pension fund data compliance. This system combines Excel/CSV file processing, MongoDB storage, and AI-driven analysis using Ollama/Mistral for comprehensive data validation and reporting.

> **Finance Data Validator** – An AI-powered tool that validates financial datasets against a given set of rules. Upload a rules file and a data file, and the tool checks for compliance, highlights errors, detects inconsistencies, and provides a detailed data quality report in plain language.

## 🌟 Features

### Core Functionality
- **Multi-Sheet Excel Processing**: Handles complex Excel files with multiple sheets
- **Intelligent Sheet Mapping**: Automatic and manual mapping between SRS (System Requirements Specification) and data sheets
- **AI-Powered Validation**: Uses Ollama with Mistral model for intelligent explanations and summaries
- **MongoDB Integration**: Complete data persistence with GridFS for file storage
- **Real-time Web Interface**: Streamlit-based dashboard for easy interaction

### Advanced Capabilities
- **Fuzzy Sheet Name Matching**: Handles variations in sheet naming conventions
- **Comprehensive Error Handling**: Robust error reporting and debugging tools
- **Validation History**: Track all validation results and AI responses
- **File Storage**: Secure storage of uploaded files with metadata
- **Interactive Dashboard**: User-friendly interface with progress indicators

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB Server
- Ollama (for AI functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/manushukla2/data-validator-ai.git
   cd data-validator-ai
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .\.venv\Scripts\Activate.ps1
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and setup Ollama**
   ```bash
   # Install Ollama (Windows)
   winget install Ollama.Ollama
   
   # Pull Mistral model
   ollama pull mistral
   ```

5. **Start MongoDB**
   - Ensure MongoDB server is running on localhost:27017

6. **Run the application**
   ```bash
   streamlit run app.py --server.port 8504
   ```

## 📁 Project Structure

```
data-validator-ai/
├── app.py                              # Main Streamlit application
├── srs_parser.py                       # Excel/CSV file parsing utilities
├── data_validator.py                   # Core validation logic
├── ollama_agent.py                     # AI integration with Ollama/Mistral
├── mongodb_service.py                  # Database operations and GridFS
├── requirements.txt                    # Python dependencies
├── debug_excel.py                      # Debugging utilities
├── test_mongodb.py                     # Database connection testing
├── create_test_files.py                # Test data generation
└── README.md                           # This file
```

## 🔧 Configuration

### MongoDB Setup
The application expects MongoDB running on:
- **Host**: localhost
- **Port**: 27017
- **Database**: data_validator

### Ollama Configuration
Make sure Ollama is running with the Mistral model:
```bash
ollama serve
ollama pull mistral
```

## 📖 Usage

### Basic Workflow

1. **Start the Application**
   - Run `streamlit run app.py --server.port 8504`
   - Open browser to `http://localhost:8504`

2. **Upload Files**
   - Upload SRS file (contains validation rules/specifications)
   - Upload data file (contains actual data to validate)

3. **Sheet Mapping**
   - System automatically tries to match sheet names
   - Use manual mapping interface if automatic matching fails
   - Map SRS sheets to corresponding data sheets

4. **Validation & Analysis**
   - Review validation results with AI explanations
   - Get comprehensive data summaries
   - View historical validation data

### File Format Requirements

- **Supported Formats**: Excel (.xlsx), CSV (.csv)
- **SRS Files**: Should contain validation rules/specifications
- **Data Files**: Should contain actual data to be validated
- **Multi-Sheet Support**: Both Excel formats with multiple sheets

## 🗄️ Database Schema

### Collections

- **uploaded_files**: File metadata and GridFS references
- **validation_results**: Validation outcomes and summaries
- **ai_responses**: AI-generated explanations and analyses
- **fs.files/fs.chunks**: GridFS file storage

## 🤖 AI Integration

The system uses Ollama with the Mistral model for:
- **Validation Explanations**: Detailed analysis of validation failures
- **Data Summaries**: Comprehensive data sheet insights
- **Error Analysis**: Intelligent error categorization and suggestions

## 🛠️ Development

### Adding New Validation Rules
1. Modify `data_validator.py`
2. Add rule logic in validation functions
3. Update AI prompts in `ollama_agent.py` for better explanations

### Database Extensions
1. Extend `mongodb_service.py` for new collections
2. Add corresponding methods for data operations
3. Update Streamlit interface for new features

## 🔍 Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Ensure MongoDB server is running
   - Check connection string in `mongodb_service.py`

2. **Ollama Not Responding**
   - Verify Ollama is running: `ollama serve`
   - Check if Mistral model is downloaded: `ollama list`

3. **Sheet Mapping Issues**
   - Use manual mapping interface
   - Check sheet names in uploaded files
   - Verify file format compatibility

## 📊 Monitoring

Use MongoDB Compass to monitor:
- Database connection: `mongodb://localhost:27017`
- Collections and document counts
- GridFS file storage usage
- Validation result trends

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ollama** for local AI model hosting
- **Streamlit** for the web interface framework
- **MongoDB** for data persistence
- **Pandas** for data processing capabilities

---

**Built with ❤️ for pension fund data compliance and validation**
