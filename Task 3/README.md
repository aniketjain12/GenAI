# 🏗️ AI Architecture Pipeline

An AI-powered automation tool that converts high-level business requirements into detailed low-level technical specifications using Cohere AI.

## 📋 Overview

This tool simplifies the translation of business ideas into technical designs by automatically generating:
- **Requirement Analysis** - Actors, actions, entities, and relationships
- **Module Design** - System modules with interfaces and interactions
- **Database Schema** - Tables, fields, relationships, and constraints
- **Pseudocode** - Implementation logic for core functionalities

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Architecture Pipeline                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Business   │───▶│  Requirement │───▶│    Module    │       │
│  │ Requirement  │    │   Analyzer   │    │  Identifier  │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                 │                │
│                      ┌──────────────────────────┘                │
│                      ▼                                           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Output     │◀───│  Pseudocode  │◀───│    Schema    │       │
│  │  Formatter   │    │  Generator   │    │  Generator   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Pipeline Stages

| Stage | Description | Input | Output |
|-------|-------------|-------|--------|
| **Requirement Analyzer** | Parses business requirements to identify actors, actions, and entities | Raw requirement text | Structured analysis |
| **Module Identifier** | Designs system modules based on analysis | Analysis results | Module architecture |
| **Schema Generator** | Creates database schema from entities | Analysis + Modules | Database design |
| **Pseudocode Generator** | Generates implementation logic | All previous outputs | Pseudocode + APIs |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Cohere API key (get one at [cohere.com](https://cohere.com))

### Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Cohere API key**
   
   **Option 1: Create a `.env` file (Recommended)**
   ```bash
   # Create .env file in project root
   echo COHERE_API_KEY=your-api-key-here > .env
   ```
   
   **Option 2: Set environment variable**
   ```bash
   # Windows PowerShell
   $env:COHERE_API_KEY = "your-api-key-here"
   
   # Windows Command Prompt
   set COHERE_API_KEY=your-api-key-here
   
   # Linux/macOS
   export COHERE_API_KEY="your-api-key-here"
   ```

### Usage

You can use either the **Web Interface (Streamlit)** or **Command Line (CLI)**.

#### 🌐 Web Interface (Recommended)
```bash
python -m streamlit run app.py
```
This opens a user-friendly web interface at `http://localhost:8501` with:
- API key configuration
- Sample requirements to test
- Interactive progress tracking
- Tabbed output display
- Download buttons for results

#### 💻 Command Line Interface

**Interactive Mode (Default)**
```bash
python main.py
```

**Direct Requirement Input**
```bash
python main.py -r "Create a blog system with user authentication"
```

**From File**
```bash
python main.py --file sample_input.txt --output my_specs
```

**Demo Mode**
```bash
python main.py --demo
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-r, --requirement` | Business requirement text to process |
| `-f, --file` | Path to file containing the requirement |
| `-o, --output` | Output file path (without extension) |
| `--format` | Output format: `markdown` or `json` (default: markdown) |
| `--model` | Cohere model to use (default: command-a-03-2025) |
| `-i, --interactive` | Run in interactive mode |
| `--demo` | Run demonstration with sample requirement |
| `-q, --quiet` | Suppress verbose output |

## 📁 Project Structure

```
Task 3/
├── main.py                 # CLI entry point
├── app.py                  # Streamlit web application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .env                    # Environment variables (API key)
├── sample_input.txt        # Sample input requirement
├── outputs/                # Generated specifications
│   ├── sample_output.md
│   └── *.md/*.json         # Your generated outputs
├── pipeline/               # Pipeline package
│   ├── __init__.py
│   ├── base.py             # Base class for pipeline stages
│   ├── analyzer.py         # Stage 1: Requirement Analyzer
│   ├── module_identifier.py # Stage 2: Module Identifier
│   ├── schema_generator.py  # Stage 3: Schema Generator
│   ├── pseudocode_generator.py # Stage 4: Pseudocode Generator
│   └── pipeline.py         # Pipeline orchestrator
└── utils/                  # Utility modules
    ├── __init__.py
    └── formatter.py        # Output formatter (Markdown/JSON)
```

## 📝 Sample Input/Output

### Input
```
Create a system where users can register, log in, and place orders.
```

### Output Summary
The tool generates a comprehensive technical specification including:

1. **Requirement Analysis**
   - Actors: User, System, Admin
   - Actions: Register, Login, Place Order, View Orders
   - Entities: User, Order, OrderItem, Product, Session

2. **Module Design**
   - AuthenticationModule
   - UserModule
   - OrderModule
   - ProductModule

3. **Database Schema**
   - users, sessions, products, orders, order_items tables
   - Proper relationships and indexes

4. **Pseudocode**
   - Registration, login, order creation functions
   - Data flows and API contracts

See [outputs/sample_output.md](outputs/sample_output.md) for a complete example.

## 🔧 Configuration

You can customize the pipeline behavior through `config.py` or command-line arguments:

```python
from config import PipelineConfig

config = PipelineConfig(
    cohere_api_key="your-key",  # Or set COHERE_API_KEY env var
    model_name="command-a-03-2025",  # Cohere's latest model
    temperature=0.7,            # Creativity level (0.0-1.0)
    max_tokens=2000,            # Max response length per stage
    output_format="markdown",   # 'markdown' or 'json'
    verbose=True                # Show progress in console
)
```

### Environment Variables

Create a `.env` file in the project root:
```bash
COHERE_API_KEY=your-cohere-api-key-here
```

## 🧪 How It Works

1. **Input Processing**: The business requirement is received and validated

2. **Stage 1 - Analysis**: AI analyzes the requirement to extract:
   - Actors (users, systems)
   - Actions (verbs, operations)
   - Entities (nouns, data objects)
   - Relationships and business rules

3. **Stage 2 - Module Design**: Based on the analysis, AI designs:
   - Logical system modules
   - Module interfaces and methods
   - Dependencies and interactions
   - Cross-cutting concerns

4. **Stage 3 - Schema Design**: AI generates:
   - Database tables with fields
   - Data types and constraints
   - Relationships and indexes
   - Enums and validations

5. **Stage 4 - Pseudocode**: AI produces:
   - Function implementations
   - Error handling
   - Data flows
   - API contracts

6. **Output Formatting**: Results are formatted as Markdown or JSON

## 🎯 Design Principles

- **Modular Architecture**: Each pipeline stage is independent and testable
- **Single Responsibility**: Each module has one clear purpose
- **Extensibility**: Easy to add new stages or modify existing ones
- **Clean Output**: Structured, readable specifications

## ⚠️ Limitations

- Designed for simple to medium complexity requirements
- Assumes a generic backend application context
- AI-generated output should be reviewed by developers
- Token limits may affect very complex requirements

## 🔒 Security Notes

- Never commit your Cohere API key
- Use environment variables for sensitive configuration
- Review generated schemas for security best practices

## 🖥️ Streamlit Web Interface

The web interface provides an intuitive way to use the pipeline:

### Features
- **Sidebar Configuration**: API key, model selection, temperature, max tokens
- **Sample Requirements**: Pre-built examples (E-commerce, Blog, Task Management, Inventory)
- **Progress Tracking**: Visual progress bar for each pipeline stage
- **Tabbed Output Display**:
  - 🔍 Requirement Analysis
  - 🧩 Module Design  
  - 🗄️ Database Schema
  - 💻 Pseudocode
  - 📄 Raw Output
- **Download Options**: Export as Markdown or JSON
- **Auto-save**: Results saved to `outputs/` folder

### Screenshots

```
┌─────────────────────────────────────────────────────────────────┐
│  🏗️ AI Architecture Pipeline                                    │
│  Convert Business Requirements into Technical Specifications     │
├─────────────────────────────────────────────────────────────────┤
│  ⚙️ Configuration    │  📋 Business Requirement                 │
│  ─────────────────   │  ┌─────────────────────────────────────┐ │
│  API Key: ●●●●●●●●   │  │ Create a system where users can     │ │
│  Model: command-a... │  │ register, log in, and place orders. │ │
│  Temperature: 0.7    │  └─────────────────────────────────────┘ │
│                      │                                          │
│  📝 Sample Reqs      │  [🚀 Generate Technical Specification]   │
│  ○ E-commerce        │                                          │
│  ○ Blog Platform     │──────────────────────────────────────────│
│  ○ Task Management   │  📊 Results                              │
│                      │  [Analysis][Modules][Schema][Pseudocode] │
└─────────────────────────────────────────────────────────────────┘
```

## 📄 License

This project is provided as a prototype/demonstration tool.

---

