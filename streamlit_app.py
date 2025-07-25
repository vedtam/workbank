"""
WORKBank Streamlit Dashboard

This is a basic Streamlit frontend for displaying initial WORKBank results.

Installation Instructions:
1. Install Streamlit: pip install streamlit
2. Run the app: streamlit run streamlit_app.py
3. The app will open in your browser at http://localhost:8501

The app displays sample worker desire and AI capability data from the WORKBank project.
"""

import streamlit as st

# Sample result dictionaries representing WORKBank data
sample_results = [
    {
        "task": "Create marketing materials and promotional content",
        "occupation": "Marketing Managers",
        "automation_desire_rating": 4.2,
        "job_security_rating": 3.1,
        "enjoyment_rating": 3.8,
        "expert_capability_rating": 3.5,
        "worker_count": 45
    },
    {
        "task": "Analyze customer feedback and survey responses", 
        "occupation": "Market Research Analysts",
        "automation_desire_rating": 4.7,
        "job_security_rating": 2.8,
        "enjoyment_rating": 2.9,
        "expert_capability_rating": 4.1,
        "worker_count": 38
    },
    {
        "task": "Schedule appointments and manage calendars",
        "occupation": "Administrative Assistants", 
        "automation_desire_rating": 4.9,
        "job_security_rating": 2.3,
        "enjoyment_rating": 2.1,
        "expert_capability_rating": 4.8,
        "worker_count": 52
    },
    {
        "task": "Provide emotional support and counseling to patients",
        "occupation": "Clinical Social Workers",
        "automation_desire_rating": 1.2,
        "job_security_rating": 4.8,
        "enjoyment_rating": 4.9,
        "expert_capability_rating": 1.5,
        "worker_count": 29
    },
    {
        "task": "Write and edit technical documentation",
        "occupation": "Technical Writers",
        "automation_desire_rating": 3.4,
        "job_security_rating": 3.6,
        "enjoyment_rating": 4.1,
        "expert_capability_rating": 3.8,
        "worker_count": 33
    }
]

def main():
    # Title
    st.title("🤖 WORKBank: AI Agent Worker Outlook Dashboard")
    
    # Header
    st.header("Initial Results: Worker Desire vs AI Capability")
    
    # Introduction text
    st.markdown("""
    This dashboard displays sample results from the WORKBank database, which captures worker desire 
    and technological capability of AI agents for occupational tasks across the U.S. workforce.
    """)
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Tasks Analyzed", 
            value=len(sample_results)
        )
    
    with col2:
        avg_automation_desire = sum(r["automation_desire_rating"] for r in sample_results) / len(sample_results)
        st.metric(
            label="Avg Automation Desire", 
            value=f"{avg_automation_desire:.1f}/5.0"
        )
    
    with col3:
        total_workers = sum(r["worker_count"] for r in sample_results)
        st.metric(
            label="Total Workers Surveyed", 
            value=total_workers
        )
    
    # Results section
    st.subheader("Task Analysis Results")
    
    # Iterate over sample results and display them
    for i, result in enumerate(sample_results, 1):
        with st.expander(f"Task {i}: {result['task'][:50]}{'...' if len(result['task']) > 50 else ''}"):
            
            # Task details
            st.markdown(f"**Occupation:** {result['occupation']}")
            st.markdown(f"**Full Task:** {result['task']}")
            st.markdown(f"**Workers Surveyed:** {result['worker_count']}")
            
            # Ratings in columns
            rating_col1, rating_col2 = st.columns(2)
            
            with rating_col1:
                st.markdown("**Worker Ratings:**")
                st.progress(result['automation_desire_rating'] / 5.0, text=f"Automation Desire: {result['automation_desire_rating']}/5.0")
                st.progress(result['job_security_rating'] / 5.0, text=f"Job Security: {result['job_security_rating']}/5.0") 
                st.progress(result['enjoyment_rating'] / 5.0, text=f"Task Enjoyment: {result['enjoyment_rating']}/5.0")
            
            with rating_col2:
                st.markdown("**Expert Assessment:**")
                st.progress(result['expert_capability_rating'] / 5.0, text=f"AI Capability: {result['expert_capability_rating']}/5.0")
                
                # Calculate automation readiness (alignment between desire and capability)
                readiness = min(result['automation_desire_rating'], result['expert_capability_rating'])
                st.progress(readiness / 5.0, text=f"Automation Readiness: {readiness:.1f}/5.0")
            
            # Analysis insight
            if result['automation_desire_rating'] > result['expert_capability_rating']:
                st.info("📈 Workers want more automation than current AI capability allows")
            elif result['automation_desire_rating'] < result['expert_capability_rating']:
                st.warning("⚠️ AI capability exceeds worker desire for automation")
            else:
                st.success("✅ Worker desire aligns with AI capability")
    
    # Data visualization section
    st.subheader("Data Visualization")
    
    # Create a simple chart comparing desire vs capability
    import pandas as pd
    import matplotlib.pyplot as plt
    
    # Prepare data for visualization
    chart_data = pd.DataFrame(sample_results)
    chart_data['task_short'] = chart_data['task'].str[:30] + '...'
    
    # Create comparison chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x_pos = range(len(chart_data))
    width = 0.35
    
    ax.bar([x - width/2 for x in x_pos], chart_data['automation_desire_rating'], 
           width, label='Worker Automation Desire', alpha=0.8, color='steelblue')
    ax.bar([x + width/2 for x in x_pos], chart_data['expert_capability_rating'], 
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
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **About WORKBank:** This database captures worker desire and technological capability of AI agents 
    for occupational tasks, featuring preferences from 1,500 U.S. domain workers and capability 
    assessments from AI experts across 844 tasks and 104 occupations.
    
    📄 [Read the full paper](https://arxiv.org/abs/2506.06576) | 
    🗃️ [Access the dataset](https://huggingface.co/datasets/SALT-NLP/WORKBank)
    """)

if __name__ == "__main__":
    main()