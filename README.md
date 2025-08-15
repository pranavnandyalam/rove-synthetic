# Rove Synthetic – Airline Miles Redemption Optimizer

> **Smart recommendations for maximizing your airline miles value**

Rove Synthetic is an intelligent web application that helps travelers find the best ways to spend their airline miles by calculating value-per-mile (VPM) and ranking redemption options across flights, hotels, and cash alternatives.

## 🚀 Features

- **Value-Per-Mile Calculator**: Automatically computes the dollar value you get per mile spent
- **Smart Flight Recommendations**: Searches real flight data via Amadeus API and ranks by best value
- **Multi-Category Comparison**: Compares flights, hotels, and gift cards to show your best options
- **Affordability Filtering**: Shows what you can actually book with your available miles
- **Fallback System**: Works even when external APIs are unavailable (uses realistic mock data)
- **User Feedback Collection**: Stores user ratings to improve recommendations over time
- **Modern Web Interface**: Clean, responsive UI built with Flask and Tailwind CSS

## 🏗️ Architecture

The system is built with a clean, layered architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Layer     │    │ Business Logic  │    │  Data Layer     │
│   (Flask)       │◄──►│ (Recommender)   │◄──►│ (Amadeus API)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Templates     │    │   Routing       │    │   Mock Data     │
│   (HTML/CSS)    │    │ (Data Processing)│   │   (Fallback)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components

- **`app.py`** - Flask web server and route handlers
- **`recommender.py`** - Main recommendation engine and business logic
- **`routing.py`** - Flight data processing and VPM calculations
- **`value_calc.py`** - Value-per-mile math and industry benchmarks
- **`reference.py`** - Amadeus API integration for real flight data
- **`sql_lite.py`** - User feedback storage and analytics

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Rove-Synthetic
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required for web app security
APP_SECRET_KEY=your_secret_key_here

# Optional: Amadeus API credentials for live flight data
AMADEUS_API_KEY=your_amadeus_api_key
AMADEUS_API_SECRET=your_amadeus_api_secret

# Optional: Skyscanner API for additional flight data
SKYSCANNER_API_KEY=your_skyscanner_api_key
```

### API Credentials

- **Amadeus API**: Get free credentials at [Amadeus for Developers](https://developers.amadeus.com/)
- **Without API keys**: The system automatically falls back to realistic mock data

## 📊 How It Works

### 1. Value-Per-Mile Calculation

The system calculates how much value you get per mile:

```
VPM = (Cash Price - Taxes & Fees) / Miles Used
```

**Example**: A $350 flight with $5.60 taxes using 26,500 miles:
- VPM = ($350 - $5.60) / 26,500 = $0.013 per mile = **1.3¢ per mile**

### 2. Industry Benchmarks

The system uses accepted industry standards to determine "good value":

- **Flight Awards**: 1.3¢/mile (baseline for good flight redemptions)
- **Hotel Awards**: 0.7¢/point (baseline for hotel redemptions)
- **Gift Cards**: 0.5¢/point (baseline for cash alternatives)

### 3. Recommendation Process

1. **Search Flights**: Query Amadeus API for available flights
2. **Calculate VPM**: Compute value-per-mile for each option
3. **Filter by Affordability**: Show only flights you can book with your miles
4. **Add Comparisons**: Include hotel and gift card alternatives
5. **Rank by Value**: Sort everything by best VPM first
6. **Display Results**: Show top recommendations with rationale

## 🧪 Testing

Run the test suite to verify everything works:

```bash
python test_requirements.py
```

Or run individual tests:

```bash
python -m unittest test_requirements.py
```

## 📁 Project Structure

```
Rove-Synthetic/
├── app.py                 # Flask web application
├── recommender.py         # Main recommendation engine
├── routing.py            # Flight data processing
├── value_calc.py         # VPM calculations
├── reference.py          # Amadeus API integration
├── sql_lite.py           # Database operations
├── main.py               # CLI entry point
├── templates/            # HTML templates
│   ├── layout.html      # Base template
│   └── index.html       # Main page
├── .env                 # Environment variables
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Development

### Adding New Features

1. **Business Logic**: Add functions to `value_calc.py` or `routing.py`
2. **API Integration**: Extend `reference.py` for new data sources
3. **Web Interface**: Modify templates in `templates/` directory
4. **Database**: Update `sql_lite.py` for new data storage

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints for function parameters and return values
- Add docstrings for all public functions
- Include error handling for external API calls

## 🚀 Deployment

### Local Development

```bash
python app.py
```

### Production Deployment

For production, consider:

- **WSGI Server**: Use Gunicorn or uWSGI
- **Reverse Proxy**: Nginx for static files and load balancing
- **Environment**: Set `FLASK_ENV=production`
- **Database**: Consider PostgreSQL for larger scale
- **Monitoring**: Add logging and health checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Amadeus API** for flight data
- **Flask** for the web framework
- **Tailwind CSS** for the UI design
- **Python community** for excellent libraries

## 📞 Support

- **Issues**: Report bugs via GitHub Issues
- **Questions**: Open a GitHub Discussion
- **Contributions**: Submit Pull Requests

---

**Built with ❤️ for travelers who want to maximize their miles value** 