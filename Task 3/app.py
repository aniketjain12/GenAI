"""
Streamlit Web Application for AI Architecture Pipeline
A user-friendly interface to convert business requirements into technical specifications.
"""

import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import pipeline components
from config import PipelineConfig
from pipeline import ArchitecturePipeline
from utils.formatter import OutputFormatter

# Page configuration
st.set_page_config(
    page_title="AI Architecture Pipeline",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stage-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1E88E5;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e7f3ff;
        border: 1px solid #b6d4fe;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'history' not in st.session_state:
        st.session_state.history = []


def get_cohere_client(api_key: str, model: str, temperature: float, max_tokens: int):
    """Initialize and return Cohere client with config."""
    try:
        import cohere
        client = cohere.ClientV2(api_key=api_key)
        config = PipelineConfig(
            cohere_api_key=api_key,
            model_name=model,
            temperature=temperature,
            max_tokens=max_tokens,
            verbose=False
        )
        return client, config
    except Exception as e:
        st.error(f"Failed to initialize Cohere client: {str(e)}")
        return None, None


def run_pipeline_with_progress(requirement: str, client, config):
    """Run the pipeline with progress indicators."""
    pipeline = ArchitecturePipeline(client, config)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    stages = [
        ("Analyzing Requirements", 0.25),
        ("Identifying Modules", 0.50),
        ("Generating Schema", 0.75),
        ("Creating Pseudocode", 1.0)
    ]
    
    try:
        # Run the pipeline
        status_text.text("Starting pipeline...")
        result = pipeline.run(requirement)
        
        progress_bar.progress(1.0)
        status_text.text("Pipeline completed successfully!")
        
        return result
    except Exception as e:
        st.error(f"Pipeline failed: {str(e)}")
        return None


def display_requirement_analysis(analysis: dict):
    """Display the requirement analysis section."""
    if not analysis or 'raw_response' in analysis:
        st.warning("Could not parse requirement analysis.")
        return
    
    # Summary
    if analysis.get('requirement_summary'):
        st.markdown(f"**Summary:** {analysis['requirement_summary']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Actors
        st.markdown("#### 👥 Actors")
        actors = analysis.get('actors', [])
        if actors:
            for actor in actors:
                with st.expander(f"**{actor.get('name', 'Unknown')}** ({actor.get('type', 'N/A')})"):
                    st.write(actor.get('description', 'No description'))
        else:
            st.info("No actors identified")
        
        # Entities
        st.markdown("#### 📦 Entities")
        entities = analysis.get('entities', [])
        if entities:
            for entity in entities:
                with st.expander(f"**{entity.get('name', 'Unknown')}**"):
                    st.write(f"*{entity.get('description', 'No description')}*")
                    attrs = entity.get('attributes', [])
                    if attrs:
                        st.write("**Attributes:**", ", ".join([f"`{a}`" for a in attrs]))
        else:
            st.info("No entities identified")
    
    with col2:
        # Actions
        st.markdown("#### ⚡ Actions")
        actions = analysis.get('actions', [])
        if actions:
            for action in actions:
                priority = action.get('priority', 'medium')
                priority_color = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority, '⚪')
                with st.expander(f"{priority_color} **{action.get('name', 'Unknown')}**"):
                    st.write(f"**Actor:** {action.get('actor', 'N/A')}")
                    st.write(f"**Description:** {action.get('description', 'N/A')}")
        else:
            st.info("No actions identified")
        
        # Business Rules
        st.markdown("#### 📋 Business Rules")
        rules = analysis.get('business_rules', [])
        if rules:
            for i, rule in enumerate(rules, 1):
                st.markdown(f"{i}. {rule}")
        else:
            st.info("No business rules identified")


def display_modules(modules: dict):
    """Display the module design section."""
    if not modules or 'raw_response' in modules:
        st.warning("Could not parse module design.")
        return
    
    # Overview
    if modules.get('system_overview'):
        st.markdown(f"**System Overview:** {modules['system_overview']}")
    
    if modules.get('architecture_pattern'):
        st.markdown(f"**Architecture Pattern:** `{modules['architecture_pattern']}`")
    
    st.markdown("---")
    
    # Modules
    module_list = modules.get('modules', [])
    if module_list:
        cols = st.columns(min(3, len(module_list)))
        for i, module in enumerate(module_list):
            with cols[i % 3]:
                st.markdown(f"### 📦 {module.get('name', 'Unknown')}")
                st.markdown(f"**Type:** `{module.get('type', 'N/A')}`")
                st.markdown(f"**Purpose:** {module.get('purpose', 'N/A')}")
                
                # Responsibilities
                responsibilities = module.get('responsibilities', [])
                if responsibilities:
                    with st.expander("Responsibilities"):
                        for resp in responsibilities:
                            st.markdown(f"- {resp}")
                
                # Interfaces
                interfaces = module.get('interfaces', [])
                if interfaces:
                    with st.expander("Interfaces"):
                        for iface in interfaces:
                            st.markdown(f"**`{iface.get('name', 'method')}`**")
                            st.markdown(f"  - Inputs: {', '.join(iface.get('inputs', []))}")
                            st.markdown(f"  - Output: {iface.get('outputs', 'void')}")
    else:
        st.info("No modules identified")
    
    # Cross-cutting Concerns
    concerns = modules.get('cross_cutting_concerns', [])
    if concerns:
        st.markdown("---")
        st.markdown("### 🔄 Cross-cutting Concerns")
        for concern in concerns:
            st.markdown(f"- **{concern.get('name', 'Unknown')}:** {concern.get('description', 'N/A')}")


def display_schema(schema: dict):
    """Display the database schema section."""
    if not schema or 'raw_response' in schema:
        st.warning("Could not parse database schema.")
        return
    
    # Database type
    if schema.get('database_type'):
        st.markdown(f"**Database Type:** `{schema['database_type']}`")
    
    st.markdown("---")
    
    # Tables
    tables = schema.get('tables', [])
    if tables:
        for table in tables:
            st.markdown(f"### 📊 {table.get('name', 'Unknown')}")
            if table.get('description'):
                st.markdown(f"*{table['description']}*")
            
            # Fields
            fields = table.get('fields', [])
            if fields:
                field_data = []
                for field in fields:
                    key_icon = ""
                    if field.get('primary_key'):
                        key_icon = "🔑 PK"
                    elif field.get('foreign_key'):
                        key_icon = "🔗 FK"
                    
                    field_data.append({
                        "Field": field.get('name', 'N/A'),
                        "Type": field.get('data_type', 'N/A'),
                        "Nullable": "Yes" if field.get('nullable') else "No",
                        "Key": key_icon,
                        "Description": field.get('description', '')[:50]
                    })
                
                st.dataframe(field_data, use_container_width=True, hide_index=True)
            
            st.markdown("")
    else:
        st.info("No tables generated")
    
    # Relationships
    relationships = schema.get('relationships', [])
    if relationships:
        st.markdown("### 🔗 Relationships")
        for rel in relationships:
            st.markdown(f"- `{rel.get('from_table', 'N/A')}` → `{rel.get('to_table', 'N/A')}` ({rel.get('type', 'N/A')})")


def display_pseudocode(pseudocode: dict):
    """Display the pseudocode section."""
    if not pseudocode or 'raw_response' in pseudocode:
        st.warning("Could not parse pseudocode.")
        return
    
    # Functions
    functions = pseudocode.get('functions', [])
    if functions:
        st.markdown("### 📝 Functions")
        for func in functions:
            func_name = f"{func.get('module', 'Module')}.{func.get('name', 'function')}"
            with st.expander(f"**{func_name}**"):
                st.markdown(f"*{func.get('description', 'No description')}*")
                
                # Parameters
                params = func.get('parameters', [])
                if params:
                    st.markdown("**Parameters:**")
                    for param in params:
                        st.markdown(f"- `{param.get('name', 'param')}` ({param.get('type', 'Any')}): {param.get('description', '')}")
                
                # Returns
                returns = func.get('returns', {})
                if returns:
                    st.markdown(f"**Returns:** `{returns.get('type', 'void')}` - {returns.get('description', '')}")
                
                # Pseudocode
                code = func.get('pseudocode', [])
                if code:
                    st.markdown("**Code:**")
                    st.code("\n".join(code), language="text")
                
                # Complexity
                complexity = func.get('complexity', {})
                if complexity:
                    st.markdown(f"**Complexity:** Time: {complexity.get('time', 'N/A')}, Space: {complexity.get('space', 'N/A')}")
    else:
        st.info("No functions generated")
    
    # Data Flows
    flows = pseudocode.get('data_flows', [])
    if flows:
        st.markdown("---")
        st.markdown("### 🔄 Data Flows")
        for flow in flows:
            with st.expander(f"**{flow.get('name', 'Flow')}**"):
                st.markdown(f"*{flow.get('description', '')}*")
                steps = flow.get('steps', [])
                if steps:
                    for step in steps:
                        st.markdown(f"{step.get('step', '-')}. **{step.get('action', 'Action')}** → `{step.get('function', 'N/A')}`")
    
    # API Contracts
    apis = pseudocode.get('api_contracts', [])
    if apis:
        st.markdown("---")
        st.markdown("### 🌐 API Contracts")
        for api in apis:
            method = api.get('method', 'GET')
            endpoint = api.get('endpoint', '/api')
            with st.expander(f"**{method}** `{endpoint}`"):
                st.markdown(f"*{api.get('description', '')}*")
                
                if api.get('request_body'):
                    st.markdown("**Request Body:**")
                    st.json(api['request_body'])
                
                if api.get('response'):
                    st.markdown("**Response:**")
                    st.json(api['response'])
                
                status_codes = api.get('status_codes', [])
                if status_codes:
                    st.markdown("**Status Codes:**")
                    for sc in status_codes:
                        st.markdown(f"- `{sc.get('code', '')}`: {sc.get('description', '')}")


def save_output(result: dict, filename: str, format_type: str):
    """Save output to file."""
    outputs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    
    if format_type == "markdown":
        content = OutputFormatter.to_markdown(result)
        extension = ".md"
    else:
        content = OutputFormatter.to_json(result)
        extension = ".json"
    
    filepath = os.path.join(outputs_dir, f"{filename}{extension}")
    OutputFormatter.save_to_file(content, filepath)
    return filepath


def main():
    """Main application function."""
    init_session_state()
    
    # Header
    st.markdown('<p class="main-header">🏗️ AI Architecture Pipeline</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Convert Business Requirements into Technical Specifications</p>', unsafe_allow_html=True)
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key
        api_key = st.text_input(
            "Cohere API Key",
            value=os.getenv("COHERE_API_KEY", ""),
            type="password",
            help="Enter your Cohere API key"
        )
        
        # Model Selection
        model = st.selectbox(
            "Model",
            options=["command-a-03-2025", "command-r-08-2024", "command-r7b-12-2024"],
            index=0,
            help="Select the Cohere model to use"
        )
        
        # Advanced Settings
        with st.expander("Advanced Settings"):
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values make output more creative"
            )
            
            max_tokens = st.slider(
                "Max Tokens",
                min_value=500,
                max_value=4000,
                value=2000,
                step=100,
                help="Maximum tokens per response"
            )
        
        st.markdown("---")
        
        # Sample Requirements
        st.header("📝 Sample Requirements")
        
        samples = {
            "E-commerce System": "Create an e-commerce system where users can register, browse products, add items to cart, and place orders with payment processing.",
            "Blog Platform": "Build a blog platform where users can create accounts, write and publish articles, comment on posts, and follow other authors.",
            "Task Management": "Design a task management system where teams can create projects, assign tasks, track progress, and collaborate with comments.",
            "Inventory System": "Create an inventory management system for tracking products, managing stock levels, processing orders, and generating reports."
        }
        
        selected_sample = st.selectbox("Load Sample", options=["-- Select --"] + list(samples.keys()))
    
    # Main Content Area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Business Requirement")
        
        # Pre-fill with sample if selected
        default_text = ""
        if selected_sample and selected_sample != "-- Select --":
            default_text = samples[selected_sample]
        
        requirement = st.text_area(
            "Enter your high-level business requirement:",
            value=default_text,
            height=150,
            placeholder="Example: Create a system where users can register, log in, and place orders..."
        )
    
    with col2:
        st.subheader("📤 Output Options")
        
        output_filename = st.text_input(
            "Output Filename",
            value=f"spec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            help="Name for the output file (saved to outputs folder)"
        )
        
        output_format = st.radio(
            "Format",
            options=["Markdown", "JSON"],
            horizontal=True
        )
        
        save_to_file = st.checkbox("Save to file", value=True)
    
    # Generate Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button(
            "🚀 Generate Technical Specification",
            type="primary",
            use_container_width=True,
            disabled=not api_key or not requirement
        )
    
    if not api_key:
        st.warning("⚠️ Please enter your Cohere API key in the sidebar to continue.")
    
    # Process
    if generate_btn and api_key and requirement:
        with st.spinner("🔄 Processing your requirement..."):
            client, config = get_cohere_client(api_key, model, temperature, max_tokens)
            
            if client and config:
                result = run_pipeline_with_progress(requirement, client, config)
                
                if result:
                    st.session_state.result = result
                    
                    # Save to file if requested
                    if save_to_file:
                        format_key = "markdown" if output_format == "Markdown" else "json"
                        filepath = save_output(result, output_filename, format_key)
                        st.success(f"✅ Output saved to: `{filepath}`")
                    
                    # Add to history
                    st.session_state.history.append({
                        "timestamp": datetime.now().isoformat(),
                        "requirement": requirement[:100] + "...",
                        "filename": output_filename
                    })
    
    # Display Results
    if st.session_state.result:
        st.markdown("---")
        st.header("📊 Generated Technical Specification")
        
        result = st.session_state.result
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔍 Requirement Analysis",
            "🧩 Module Design",
            "🗄️ Database Schema",
            "💻 Pseudocode",
            "📄 Raw Output"
        ])
        
        with tab1:
            analysis = result.get('analysis', {})
            display_requirement_analysis(analysis)
        
        with tab2:
            modules = result.get('modules', {})
            display_modules(modules)
        
        with tab3:
            schema = result.get('schema', {})
            display_schema(schema)
        
        with tab4:
            pseudocode = result.get('pseudocode', {})
            display_pseudocode(pseudocode)
        
        with tab5:
            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                md_content = OutputFormatter.to_markdown(result)
                st.download_button(
                    label="📥 Download Markdown",
                    data=md_content,
                    file_name=f"{output_filename}.md",
                    mime="text/markdown"
                )
            with col2:
                json_content = OutputFormatter.to_json(result)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_content,
                    file_name=f"{output_filename}.json",
                    mime="application/json"
                )
            
            # Show raw output
            if output_format == "Markdown":
                st.markdown(md_content)
            else:
                st.json(result)
        
        # Execution Summary
        metadata = result.get('metadata', {})
        if metadata:
            st.markdown("---")
            st.markdown("### ⏱️ Execution Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Duration", f"{metadata.get('total_duration_seconds', 0):.2f}s")
            with col2:
                log = metadata.get('execution_log', [])
                successful = sum(1 for l in log if l.get('status') == 'success')
                st.metric("Stages Completed", f"{successful}/{len(log)}")
            with col3:
                st.metric("Generated At", metadata.get('generated_at', 'N/A')[:19])
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888;'>"
        "Built with ❤️ using Streamlit and Cohere AI"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
