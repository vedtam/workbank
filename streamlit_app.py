"""
WORKBank Streamlit Dashboard

This dashboard displays worker desire and AI capability data from the WORKBank project,
which captures preferences from 1,500 U.S. domain workers and capability assessments 
from AI experts across 844 tasks and 104 occupations.

Installation Instructions:
1. Install dependencies: pip install streamlit pandas matplotlib datasets
2. Run the app: streamlit run streamlit_app.py  
3. The app will open in your browser at http://localhost:8501

The app loads data from the WORKBank datasets hosted on Hugging Face.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from data_loader import load_workbank_datasets, prepare_analysis_data, get_summary_stats

@st.cache_data
def load_data():
    """Load and prepare WORKBank data."""
    worker_df, expert_df, task_df = load_workbank_datasets()
    combined_df = prepare_analysis_data(worker_df, expert_df, task_df)
    return combined_df, worker_df, expert_df, task_df


def render_overview_tab(combined_df: pd.DataFrame):
    """Render the overview tab with key metrics and high-level analysis."""
    
    st.header("WORKBank Overview")
    
    # Get summary statistics
    stats = get_summary_stats(combined_df)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Tasks Analyzed", 
            value=stats["total_tasks"]
        )
    
    with col2:
        st.metric(
            label="Avg Automation Desire", 
            value=f"{stats['avg_automation_desire']:.1f}/5.0"
        )
    
    with col3:
        st.metric(
            label="Avg AI Capability", 
            value=f"{stats['avg_expert_capability']:.1f}/5.0"
        )
    
    with col4:
        st.metric(
            label="Total Workers Surveyed", 
            value=int(stats["total_workers"])
        )
    
    # Additional metrics
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="Automation Readiness",
            value=f"{stats['avg_automation_readiness']:.1f}/5.0"
        )
    
    with col6:
        st.metric(
            label="Unique Occupations",
            value=stats["unique_occupations"]
        )
    
    with col7:
        st.metric(
            label="Unique Domains", 
            value=stats["unique_domains"]
        )
    
    with col8:
        desire_capability_gap = stats["avg_automation_desire"] - stats["avg_expert_capability"]
        st.metric(
            label="Desire-Capability Gap",
            value=f"{desire_capability_gap:+.1f}",
            delta=f"{'Workers want more' if desire_capability_gap > 0 else 'AI exceeds desire'}"
        )


def render_automation_desire_tab(combined_df: pd.DataFrame):
    """Render the automation desire analysis tab."""
    
    st.header("Automation Desire Analysis")
    
    # Filter controls
    col1, col2 = st.columns(2)
    
    with col1:
        selected_domains = st.multiselect(
            "Filter by Domain",
            options=combined_df["Domain"].unique(),
            default=combined_df["Domain"].unique()
        )
    
    with col2:
        automation_range = st.slider(
            "Automation Desire Rating Range",
            min_value=1.0,
            max_value=5.0,
            value=(1.0, 5.0),
            step=0.1
        )
    
    # Filter data
    filtered_df = combined_df[
        (combined_df["Domain"].isin(selected_domains)) &
        (combined_df["Automation Desire Rating"] >= automation_range[0]) &
        (combined_df["Automation Desire Rating"] <= automation_range[1])
    ]
    
    # Sort by automation desire
    filtered_df = filtered_df.sort_values("Automation Desire Rating", ascending=False)
    
    # Top and bottom tasks
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Highest Automation Desire")
        top_tasks = filtered_df.head(5)
        for _, task in top_tasks.iterrows():
            st.write(f"**{task['Occupation']}**")
            st.write(f"*{task['Task'][:100]}...*")
            st.write(f"Automation Desire: {task['Automation Desire Rating']:.1f}/5.0")
            st.write("---")
    
    with col2:
        st.subheader("Lowest Automation Desire")
        bottom_tasks = filtered_df.tail(5)
        for _, task in bottom_tasks.iterrows():
            st.write(f"**{task['Occupation']}**")
            st.write(f"*{task['Task'][:100]}...*")
            st.write(f"Automation Desire: {task['Automation Desire Rating']:.1f}/5.0")
            st.write("---")
    
    # Distribution plot
    st.subheader("Automation Desire Distribution")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(filtered_df["Automation Desire Rating"], bins=20, alpha=0.7, color='steelblue', edgecolor='black')
    ax.set_xlabel("Automation Desire Rating")
    ax.set_ylabel("Number of Tasks")
    ax.set_title("Distribution of Automation Desire Ratings")
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)


def render_automation_viability_tab(combined_df: pd.DataFrame):
    """Render the automation viability analysis tab."""
    
    st.header("Automation Viability Landscape")
    
    # Scatter plot of desire vs capability
    st.subheader("Worker Desire vs AI Capability")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Color by domain
    domains = combined_df["Domain"].unique()
    colors = plt.cm.Set3(np.linspace(0, 1, len(domains)))
    
    for i, domain in enumerate(domains):
        domain_data = combined_df[combined_df["Domain"] == domain]
        ax.scatter(
            domain_data["Expert Capability Rating"],
            domain_data["Automation Desire Rating"], 
            c=[colors[i]], 
            label=domain,
            alpha=0.7,
            s=100
        )
    
    # Add diagonal line for alignment
    ax.plot([1, 5], [1, 5], 'k--', alpha=0.5, linewidth=2, label='Perfect Alignment')
    
    ax.set_xlabel("Expert AI Capability Rating")
    ax.set_ylabel("Worker Automation Desire Rating") 
    ax.set_title("Automation Desire vs AI Capability by Domain")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Quadrant analysis
    st.subheader("Quadrant Analysis")
    
    col1, col2 = st.columns(2)
    
    # High desire, high capability (automation ready)
    automation_ready = combined_df[
        (combined_df["Automation Desire Rating"] >= 3.5) & 
        (combined_df["Expert Capability Rating"] >= 3.5)
    ]
    
    # High desire, low capability (automation wanted but not feasible)
    automation_wanted = combined_df[
        (combined_df["Automation Desire Rating"] >= 3.5) & 
        (combined_df["Expert Capability Rating"] < 3.5)
    ]
    
    with col1:
        st.metric(
            label="Automation Ready Tasks",
            value=len(automation_ready),
            help="High worker desire and high AI capability"
        )
        
        if len(automation_ready) > 0:
            st.write("**Top Automation Ready Tasks:**")
            for _, task in automation_ready.head(3).iterrows():
                st.write(f"• {task['Occupation']}: {task['Task'][:80]}...")
    
    with col2:
        st.metric(
            label="Automation Wanted Tasks", 
            value=len(automation_wanted),
            help="High worker desire but low AI capability"
        )
        
        if len(automation_wanted) > 0:
            st.write("**Top Automation Wanted Tasks:**")
            for _, task in automation_wanted.head(3).iterrows():
                st.write(f"• {task['Occupation']}: {task['Task'][:80]}...")


def render_task_details_tab(combined_df: pd.DataFrame):
    """Render detailed task analysis tab."""
    
    st.header("Detailed Task Analysis")
    
    # Sorting and filtering controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sort_by = st.selectbox(
            "Sort by",
            options=[
                "Automation Desire Rating",
                "Expert Capability Rating", 
                "Automation Readiness",
                "Desire Capability Gap",
                "Worker Count"
            ]
        )
    
    with col2:
        sort_order = st.selectbox(
            "Order",
            options=["Descending", "Ascending"]
        )
    
    with col3:
        show_count = st.number_input(
            "Number of tasks to show",
            min_value=5,
            max_value=len(combined_df),
            value=min(10, len(combined_df))
        )
    
    # Sort data
    ascending = sort_order == "Ascending"
    sorted_df = combined_df.sort_values(sort_by, ascending=ascending)
    
    # Display tasks
    for i, (_, task) in enumerate(sorted_df.head(show_count).iterrows(), 1):
        with st.expander(f"Task {i}: {task['Task'][:60]}{'...' if len(task['Task']) > 60 else ''}"):
            
            # Task details
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Occupation:** {task['Occupation']}")
                st.markdown(f"**Domain:** {task['Domain']}")
                st.markdown(f"**Task Category:** {task.get('Task Category', 'N/A')}")
                st.markdown(f"**Workers Surveyed:** {int(task['Worker Count'])}")
            
            with col2:
                st.markdown(f"**O*NET-SOC Code:** {task.get('O*NET-SOC Code', 'N/A')}")
                st.markdown(f"**Automation Readiness:** {task['Automation Readiness']:.1f}/5.0")
                st.markdown(f"**Desire-Capability Gap:** {task['Desire Capability Gap']:+.1f}")
            
            st.markdown(f"**Full Task:** {task['Task']}")
            
            # Ratings visualization
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Worker Ratings:**")
                st.progress(
                    task['Automation Desire Rating'] / 5.0, 
                    text=f"Automation Desire: {task['Automation Desire Rating']:.1f}/5.0"
                )
                st.progress(
                    task['Job Security Rating'] / 5.0, 
                    text=f"Job Security: {task['Job Security Rating']:.1f}/5.0"
                )
                st.progress(
                    task['Enjoyment Rating'] / 5.0, 
                    text=f"Task Enjoyment: {task['Enjoyment Rating']:.1f}/5.0"
                )
            
            with col2:
                st.markdown("**Expert Assessment:**")
                st.progress(
                    task['Expert Capability Rating'] / 5.0, 
                    text=f"AI Capability: {task['Expert Capability Rating']:.1f}/5.0"
                )
                st.progress(
                    task['Automation Readiness'] / 5.0, 
                    text=f"Automation Readiness: {task['Automation Readiness']:.1f}/5.0"
                )
                
                if 'Confidence' in task and not pd.isna(task['Confidence']):
                    st.progress(
                        task['Confidence'] / 5.0,
                        text=f"Expert Confidence: {task['Confidence']:.1f}/5.0"
                    )
            
            # Analysis insight
            if task['Automation Desire Rating'] > task['Expert Capability Rating'] + 0.5:
                st.info("📈 Workers want significantly more automation than current AI capability allows")
            elif task['Expert Capability Rating'] > task['Automation Desire Rating'] + 0.5:
                st.warning("⚠️ AI capability significantly exceeds worker desire for automation")
            else:
                st.success("✅ Worker desire reasonably aligns with AI capability")


def render_data_export_tab(combined_df: pd.DataFrame):
    """Render data export and download tab."""
    
    st.header("Data Export")
    
    st.write("Download the filtered and processed WORKBank data for your own analysis.")
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        selected_domains = st.multiselect(
            "Select Domains",
            options=combined_df["Domain"].unique(),
            default=combined_df["Domain"].unique()
        )
    
    with col2:
        selected_occupations = st.multiselect(
            "Select Occupations",
            options=combined_df["Occupation"].unique(),
            default=[]
        )
    
    # Apply filters
    filtered_df = combined_df[combined_df["Domain"].isin(selected_domains)]
    
    if selected_occupations:
        filtered_df = filtered_df[filtered_df["Occupation"].isin(selected_occupations)]
    
    st.write(f"Filtered data contains {len(filtered_df)} tasks")
    
    # Preview data
    st.subheader("Data Preview")
    st.dataframe(filtered_df.head(10))
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="workbank_filtered_data.csv",
        mime="text/csv"
    )
def main():
    # Page configuration
    st.set_page_config(
        page_title="WORKBank Dashboard",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title and description
    st.title("🤖 WORKBank: AI Agent Worker Outlook Dashboard")
    
    st.markdown("""
    **WORKBank** (AI Agent Worker Outlook and Readiness Knowledge Bank) captures worker desire 
    and technological capability of AI agents for occupational tasks across the U.S. workforce.
    
    This database features preferences from 1,500 U.S. domain workers and capability assessments 
    from AI experts, covering over 844 tasks across 104 occupations.
    """)
    
    # Load data with caching
    with st.spinner("Loading WORKBank data..."):
        combined_df, worker_df, expert_df, task_df = load_data()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    
    # Tab selection
    tab_selection = st.sidebar.radio(
        "Select Analysis",
        [
            "Overview",
            "Automation Desire",
            "Automation Viability", 
            "Task Details",
            "Data Export"
        ]
    )
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About WORKBank")
    st.sidebar.markdown("""
    - **1,500+** U.S. domain workers surveyed
    - **844** tasks analyzed
    - **104** occupations covered
    - **AI experts** provided capability assessments
    """)
    
    st.sidebar.markdown("### Resources")
    st.sidebar.markdown("""
    - 📄 [Read the paper](https://arxiv.org/abs/2506.06576)
    - 🗃️ [Access dataset](https://huggingface.co/datasets/SALT-NLP/WORKBank)
    - 🌐 [Project website](https://futureofwork.saltlab.stanford.edu/)
    """)
    
    # Render selected tab
    if tab_selection == "Overview":
        render_overview_tab(combined_df)
    elif tab_selection == "Automation Desire":
        render_automation_desire_tab(combined_df)
    elif tab_selection == "Automation Viability":
        render_automation_viability_tab(combined_df)
    elif tab_selection == "Task Details":
        render_task_details_tab(combined_df)
    elif tab_selection == "Data Export":
        render_data_export_tab(combined_df)
    
    # Legacy visualization (moved to bottom for comparison)
    if st.sidebar.checkbox("Show Legacy Chart"):
        st.markdown("---")
        st.subheader("Legacy Comparison Chart")
        
        # Create comparison chart similar to original
        chart_data = combined_df.head(10).copy()
        chart_data['task_short'] = chart_data['Task'].str[:30] + '...'
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        x_pos = range(len(chart_data))
        width = 0.35
        
        ax.bar([x - width/2 for x in x_pos], chart_data['Automation Desire Rating'], 
               width, label='Worker Automation Desire', alpha=0.8, color='steelblue')
        ax.bar([x + width/2 for x in x_pos], chart_data['Expert Capability Rating'], 
               width, label='Expert AI Capability Rating', alpha=0.8, color='lightcoral')
        
        ax.set_xlabel('Tasks')
        ax.set_ylabel('Rating (1-5 scale)')
        ax.set_title('Worker Automation Desire vs Expert AI Capability Assessment')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(chart_data['task_short'], rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)

if __name__ == "__main__":
    main()