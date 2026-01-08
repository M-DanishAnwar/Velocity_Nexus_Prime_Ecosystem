# 🚗 Velocity Nexus Prime

**A comprehensive vehicle management system for modern automobile dealerships**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![SQL Server](https://img.shields.io/badge/SQL_Server-2019%2B-green)](https://www.microsoft.com/sql-server)
[![License](https://img.shields.io/badge/License-Academic-blue)](LICENSE)

## 📋 Overview

Velocity Nexus Prime is a professional-grade vehicle management system designed to streamline dealership operations. The system provides end-to-end management of vehicle inventory, customer relationships, sales processing, and business analytics through an intuitive user interface.

Note: Separate Docs & Presentation is inside the docs/ Folder.

This project was developed as part of academic coursework at Lahore Garrison University for:
- **Database Systems** (4th Semester) - Database design and implementation
- **Software Construction & Development** (4th Semester) - Application development

## 📂 Project Structure

```
VelocityNexusPrime/
├── LAUNCHER.bat                 # One-click setup script
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment configuration template
├── database/                    # Database scripts and utilities
│   ├── schema.sql               # Complete database schema
│   ├── insert_data.sql          # Sample data initialization
│   ├── stored_procedures.sql    # Database stored procedures
│   └── backup_database.bat      # Database backup utility
├── src/                         # Source code
│   ├── database/                # Database connection layer
│   ├── repositories/            # Data access layer
│   ├── services/                # Business logic layer
│   └── ui/                      # User interface components
├── docs/                        # Documentation
│   ├── DBS_REPORT.md            # Database Systems course report
│   └── SCD_REPORT.md            # Software Construction & Development report
├── tests/                       # Unit and integration tests
├── assets/                      # Static resources (images, icons)
│   ├── icons/                   # Application icons
│   └── screenshots/             # UI screenshots
└── screenshots/                 # Application screenshots for documentation
```

## ✨ Key Features

- **Inventory Management**: Track vehicles across multiple dealerships with real-time status updates
- **Sales Processing**: Complete sales workflow with automated tax and commission calculations
- **Customer Relationship Management**: Manage customer profiles and purchase history
- **Business Analytics**: Real-time dashboard with sales trends and performance metrics
- **User Management**: Role-based access control with audit logging
- **Reporting**: Customizable reports for management decision-making

## 🛠️ Technical Stack

- **Frontend**: Python Tkinter with custom dark theme UI components
- **Backend**: Python 3.8+ with service-oriented architecture
- **Database**: Microsoft SQL Server 2019+ with 3NF normalized schema
- **Libraries**: pyodbc, matplotlib, pandas, pillow, python-dotenv
- **Tools**: Git, SSMS, VS Code

## ⚙️ Installation

### Prerequisites
- Windows 10/11
- Python 3.8 or newer
- Microsoft SQL Server 2019 Express or higher
- Git (optional, for updates)

### One-Click Setup (Recommended)
1. Download the complete project zip file
2. Extract to your preferred location (e.g., `C:\VelocityNexusPrime`)
3. Double-click `LAUNCHER.bat` file
4. Follow on-screen instructions to complete setup

### Manual Setup
```bash
# Clone repository
git clone https://github.com/yourusername/VelocityNexusPrime.git
cd Velocity_Nexus_Prime_Ecosystem

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure database connection
# 1. Copy .env.example to .env
# 2. Edit .env file with your SQL Server details

# Initialize database
python -c "from src.database.initialize import setup_database; setup_database()"

# Run application
python run.py
```

## 🖥️ Usage

1. Launch the application using `LAUNCHER.bat` or `python run.py`
2. Login with default credentials:
   - Username: `admin`
   - Password: `admin123`
3. Navigate through modules using the sidebar menu:
   - Dashboard: View key metrics and analytics
   - Inventory: Manage vehicle stock
   - Sales: Process and track sales
   - Customers: Manage customer relationships
   - Reports: Generate business insights
   - Settings: Configure application preferences
4. Access documentation through the Help menu

## 📚 Documentation

Comprehensive documentation is provided in the `docs/` directory:

- **[DBS_REPORT.md](docs/DBS_REPORT.md)**: Complete database design documentation including:
  - Entity-Relationship diagrams
  - Normalization process (1NF to BCNF)
  - SQL implementation details
  - Performance optimization strategies
  - Security considerations and backup plans

- **[SCD_REPORT.md](docs/SCD_REPORT.md)**: Software development documentation covering:
  - System architecture (3-tier design)
  - Design patterns implementation
  - Code quality standards and testing strategy
  - Deployment procedures
  - Layman's Laws of Software Development

Additional documentation is available through the application's Help menu and inline code comments.

## 🧪 Testing

The project includes comprehensive test coverage:
```bash
# Run unit tests
pytest tests/

# Check code coverage
pytest tests/ --cov=src --cov-report=html
```

Design Patterns Implemented
Singleton Pattern: Database connection management
Repository Pattern: Data access abstraction
Service Pattern: Business logic encapsulation
Factory Pattern: UI component creation standardization
Observer Pattern: Real-time UI updates
Strategy Pattern: Analytics calculation flexibility
Code Quality Standards
PEP 8 Compliance: Strict adherence to Python style guidelines
Type Hints: Comprehensive type annotations throughout codebase
Error Handling: Multi-level exception handling with logging
Test Coverage: 86% test coverage with unit and integration tests
Documentation: Complete docstrings and API documentation
Layman's Laws of Software Development
Law of Changing Requirements: "Requirements will change just after you finish implementation."
Law of Hidden Complexity: "The simplest features often hide the most complex code."
Law of Debugging Time: "Fixing bugs takes 3x longer than writing the original code."
Law of Documentation Debt: "The documentation you skip today becomes the crisis of tomorrow."
Law of Technical Debt: "Shortcuts today create compound interest in maintenance costs."
Law of User Expectations: "Users will always discover the one edge case you didn't test."
Law of Performance: "It works perfectly on your machine until shown to the client."
Deployment & Maintenance
One-click Installation: LAUNCHER.bat for simplified setup
Docker Support: Containerized deployment option
CI/CD Pipeline: GitHub Actions for automated testing and deployment
Monitoring: Comprehensive logging and performance tracking
Academic Achievement
This project demonstrates mastery of software construction principles including modular design, pattern implementation, quality assurance, and professional documentation practices. The system architecture supports both current requirements and future scalability needs.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a pull request

## 📄 License

This project is for academic purposes only and is submitted as partial fulfillment of course requirements at Lahore Garrison University. All rights reserved.

## 📞 Contact

**Development Team**:  
Muhammad Danish Anwar & Abdul Manan Arif  
Roll Numbers: SP2024 BSSE 016 & 001  
Program: BS Software Engineering (4th Semester)  

**Course Instructors**:  
- Database Systems: Sir Hafiz Qadir  
- Software Construction & Development: Ali Haider  
Institution: Lahore Garrison University

---

**Note**: This software is provided "as is" for academic demonstration purposes only. Not intended for production use without proper security review and testing.