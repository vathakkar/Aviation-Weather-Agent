# Aviation Weather Agent 🛩️

An intelligent AI-powered aviation weather assistant that helps pilots with weather analysis, flight planning, and regulatory compliance. Built with OpenAI GPT and Streamlit, this tool provides real-time METAR/TAF data, weather interpretation, and comprehensive flight planning assistance.

## ✨ Features

### 🌤️ Weather Data
- **Real-time METAR fetching** from any ICAO airport code
- **TAF (Terminal Aerodrome Forecast) retrieval** with automatic nearby airport fallback
- **Weather interpretation** - converts raw METAR/TAF into plain English
- **VFR/IFR condition analysis** with detailed flight condition assessments

### 🧠 AI-Powered Analysis
- **Intelligent flight planning** with go/no-go recommendations
- **Automatic weather analysis** using local timezone conversions
- **Proactive decision support** - anticipates pilot needs without follow-up questions
- **Regulatory compliance checking** with FAA regulation citations

### 🔍 Additional Tools
- **NOTAM retrieval** from FAA PilotWeb
- **Web search capabilities** for aviation news and updates
- **Nearby airport search** (within 20NM) when primary airport data unavailable
- **Flight planning assistance** with fuel, time, and distance calculations

### 🛡️ Safety & Reliability
- **Input validation** for all ICAO codes and parameters
- **Comprehensive error handling** with user-friendly messages
- **Request timeouts** to prevent hanging connections
- **Input sanitization** to prevent security issues
- **Logging system** for debugging and monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key
- AVWX API key (for weather data)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Aviation-Weather-Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   AVWX_API_KEY=your_avwx_api_key_here
   ```

4. **Run the application**

   **Option A: Web Interface (Recommended)**
   ```bash
   streamlit run app/frontend_chat.py
   ```
   Then open http://localhost:8501 in your browser.

   **Option B: Command Line Interface**
   ```bash
   python app/app.py
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t aviation-weather-agent .
   ```

2. **Run the container**
   ```bash
   docker run -p 80:80 -e OPENAI_API_KEY=your_key -e AVWX_API_KEY=your_key aviation-weather-agent
   ```

## 📋 Usage Examples

### Weather Queries
```
"What's the weather at KSEA?"
"Get METAR for KSFO"
"TAF for KJFK"
```

### Flight Planning
```
"Can I fly VFR from KSEA to KSFO today?"
"Plan a flight from KJFK to KBOS"
"Check weather for a night flight from KLAX to KLAS"
```

### Regulatory Questions
```
"What are the VFR fuel requirements?"
"Can I fly at night with a student pilot certificate?"
"Check NOTAMs for KORD"
```

## 🏗️ Project Structure

```
Aviation-Weather-Agent/
├── app/
│   ├── app.py                 # CLI version of the application
│   ├── frontend_chat.py       # Streamlit web interface
│   ├── config.py              # Configuration settings
│   ├── utils.py               # Utility functions
│   ├── metar_fetcher.py       # METAR data retrieval
│   ├── metar_interpreter.py   # METAR interpretation
│   ├── taf_fetcher.py         # TAF data retrieval
│   ├── taf_interpreter.py     # TAF interpretation
│   ├── notam_fetcher.py       # NOTAM retrieval
│   ├── web_search.py          # Web search functionality
│   └── prompt.yaml            # AI system prompts
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
└── README.md                  # This file
```

## 🔧 Configuration

### API Keys Required

1. **OpenAI API Key**
   - Get from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Used for AI-powered analysis and conversation

2. **AVWX API Key**
   - Get from [AVWX](https://avwx.rest/)
   - Used for real-time weather data (METAR/TAF)

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `AVWX_API_KEY`: Your AVWX API key

### Configuration Options
The application uses a centralized configuration system in `app/config.py`:
- **Model settings**: Choose between GPT-4o-mini (default) or GPT-3.5-turbo
- **Timeout settings**: Adjust request timeouts for different services
- **Error messages**: Customize error responses
- **Validation patterns**: ICAO code validation rules

## 🛡️ Safety & Disclaimer

⚠️ **Important Safety Notice**

This tool is designed to assist pilots with weather information and flight planning, but it should **NOT** be used as the sole source for flight decisions. Always:

- Verify all weather information with official sources
- Check current NOTAMs and regulatory requirements
- Consult with flight instructors or experienced pilots when in doubt
- Follow all applicable FAA regulations and procedures
- Use official aviation weather services for final flight planning

The developers are not responsible for any decisions made based on this tool's output.

## 🔒 Security Features

- **Input validation**: All user inputs are validated and sanitized
- **Error handling**: Comprehensive error handling prevents crashes
- **Timeout protection**: Requests timeout to prevent hanging
- **Logging**: API calls are logged for debugging and monitoring
- **Safe defaults**: Sensible defaults for all configuration options

## 🐛 Recent Improvements

- ✅ Fixed duplicate dependencies in requirements.txt
- ✅ Added comprehensive input validation for ICAO codes
- ✅ Improved error handling with specific error messages
- ✅ Added NOTAM functionality to both CLI and web interfaces
- ✅ Consistent model usage across all components
- ✅ Added request timeouts to prevent hanging
- ✅ Created centralized configuration system
- ✅ Added logging for debugging and monitoring
- ✅ Improved file path handling for different deployment scenarios
- ✅ Added input sanitization for security

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [AVWX](https://avwx.rest/) for weather data API
- [OpenAI](https://openai.com/) for AI capabilities
- [Streamlit](https://streamlit.io/) for the web interface
- FAA for NOTAM data access

## 📞 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

---

**Happy Flying! ✈️**