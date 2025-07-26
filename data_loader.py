"""
Data loading utilities for WORKBank Streamlit app.

This module handles loading data from HuggingFace datasets and provides
fallback mock data that matches the real dataset schema.
"""

import pandas as pd
import streamlit as st
from typing import Dict, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_workbank_datasets() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load WORKBank datasets from HuggingFace with fallback to mock data.
    
    Returns:
        Tuple of (worker_desire_df, expert_ratings_df, task_metadata_df)
    """
    try:
        # Try to load from HuggingFace
        logger.info("Attempting to load data from HuggingFace...")
        return _load_from_huggingface()
    except Exception as e:
        logger.warning(f"Failed to load from HuggingFace: {e}")
        logger.info("Using fallback mock data with real schema...")
        return _load_mock_data()


@st.cache_data(ttl=3600)  # Cache for 1 hour
def _load_from_huggingface() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load datasets from HuggingFace."""
    try:
        from datasets import load_dataset
        
        # Load worker desire data
        worker_desire = load_dataset(
            "SALT-NLP/WORKBank", 
            data_files="worker_data/domain_worker_desires.csv"
        )["train"]
        worker_df = worker_desire.to_pandas()
        
        # Load expert ratings data
        expert_ratings = load_dataset(
            "SALT-NLP/WORKBank", 
            data_files="expert_ratings/expert_rated_technological_capability.csv"
        )["train"]
        expert_df = expert_ratings.to_pandas()
        
        # Load task metadata
        task_meta_data = load_dataset(
            "SALT-NLP/WORKBank", 
            data_files="task_data/task_statement_with_metadata.csv"
        )["train"]
        task_df = task_meta_data.to_pandas()
        
        logger.info(f"Loaded {len(worker_df)} worker responses, {len(expert_df)} expert ratings, {len(task_df)} tasks")
        
        return worker_df, expert_df, task_df
        
    except ImportError as e:
        raise Exception(f"datasets library not installed: {e}")
    except Exception as e:
        raise Exception(f"Failed to load data from HuggingFace: {e}")


def _load_mock_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load mock data that matches the real WORKBank dataset schema.
    
    This is based on the structure observed in the analysis notebooks.
    """
    
    # Mock worker desire data (based on domain_worker_desires.csv schema)
    worker_data = [
        {
            "Task ID": "T001",
            "Task": "Create marketing materials and promotional content",
            "Occupation (O*NET-SOC Title)": "Marketing Managers",
            "Automation Desire Rating": 4.2,
            "Job Security Rating": 3.1,
            "Enjoyment Rating": 3.8,
            "Worker ID": "W001",
            "Domain": "Marketing"
        },
        {
            "Task ID": "T002", 
            "Task": "Analyze customer feedback and survey responses",
            "Occupation (O*NET-SOC Title)": "Market Research Analysts",
            "Automation Desire Rating": 4.7,
            "Job Security Rating": 2.8,
            "Enjoyment Rating": 2.9,
            "Worker ID": "W002",
            "Domain": "Research"
        },
        {
            "Task ID": "T003",
            "Task": "Schedule appointments and manage calendars",
            "Occupation (O*NET-SOC Title)": "Administrative Assistants",
            "Automation Desire Rating": 4.9,
            "Job Security Rating": 2.3,
            "Enjoyment Rating": 2.1,
            "Worker ID": "W003",
            "Domain": "Administration"
        },
        {
            "Task ID": "T004",
            "Task": "Provide emotional support and counseling to patients",
            "Occupation (O*NET-SOC Title)": "Clinical Social Workers",
            "Automation Desire Rating": 1.2,
            "Job Security Rating": 4.8,
            "Enjoyment Rating": 4.9,
            "Worker ID": "W004",
            "Domain": "Healthcare"
        },
        {
            "Task ID": "T005",
            "Task": "Write and edit technical documentation",
            "Occupation (O*NET-SOC Title)": "Technical Writers",
            "Automation Desire Rating": 3.4,
            "Job Security Rating": 3.6,
            "Enjoyment Rating": 4.1,
            "Worker ID": "W005",
            "Domain": "Technical"
        },
        {
            "Task ID": "T001",
            "Task": "Create marketing materials and promotional content",
            "Occupation (O*NET-SOC Title)": "Marketing Managers", 
            "Automation Desire Rating": 3.8,
            "Job Security Rating": 3.5,
            "Enjoyment Rating": 4.0,
            "Worker ID": "W006",
            "Domain": "Marketing"
        },
        {
            "Task ID": "T002",
            "Task": "Analyze customer feedback and survey responses", 
            "Occupation (O*NET-SOC Title)": "Market Research Analysts",
            "Automation Desire Rating": 4.5,
            "Job Security Rating": 3.0,
            "Enjoyment Rating": 3.2,
            "Worker ID": "W007",
            "Domain": "Research"
        }
    ]
    
    # Mock expert ratings data
    expert_data = [
        {
            "Task ID": "T001",
            "Task": "Create marketing materials and promotional content",
            "Expert Capability Rating": 3.5,
            "Expert ID": "E001",
            "Confidence": 4.2
        },
        {
            "Task ID": "T002",
            "Task": "Analyze customer feedback and survey responses",
            "Expert Capability Rating": 4.1,
            "Expert ID": "E002", 
            "Confidence": 4.5
        },
        {
            "Task ID": "T003",
            "Task": "Schedule appointments and manage calendars",
            "Expert Capability Rating": 4.8,
            "Expert ID": "E003",
            "Confidence": 4.9
        },
        {
            "Task ID": "T004",
            "Task": "Provide emotional support and counseling to patients",
            "Expert Capability Rating": 1.5,
            "Expert ID": "E004",
            "Confidence": 4.7
        },
        {
            "Task ID": "T005",
            "Task": "Write and edit technical documentation",
            "Expert Capability Rating": 3.8,
            "Expert ID": "E005",
            "Confidence": 4.0
        }
    ]
    
    # Mock task metadata
    task_metadata = [
        {
            "Task ID": "T001",
            "Task": "Create marketing materials and promotional content",
            "Occupation (O*NET-SOC Title)": "Marketing Managers",
            "O*NET-SOC Code": "11-2021.00",
            "Domain": "Marketing",
            "Task Category": "Creative"
        },
        {
            "Task ID": "T002", 
            "Task": "Analyze customer feedback and survey responses",
            "Occupation (O*NET-SOC Title)": "Market Research Analysts",
            "O*NET-SOC Code": "13-1161.00",
            "Domain": "Research",
            "Task Category": "Analytical"
        },
        {
            "Task ID": "T003",
            "Task": "Schedule appointments and manage calendars",
            "Occupation (O*NET-SOC Title)": "Administrative Assistants",
            "O*NET-SOC Code": "43-6011.00", 
            "Domain": "Administration",
            "Task Category": "Organizational"
        },
        {
            "Task ID": "T004",
            "Task": "Provide emotional support and counseling to patients",
            "Occupation (O*NET-SOC Title)": "Clinical Social Workers",
            "O*NET-SOC Code": "21-1022.00",
            "Domain": "Healthcare", 
            "Task Category": "Interpersonal"
        },
        {
            "Task ID": "T005",
            "Task": "Write and edit technical documentation",
            "Occupation (O*NET-SOC Title)": "Technical Writers",
            "O*NET-SOC Code": "27-3042.00",
            "Domain": "Technical",
            "Task Category": "Communication"
        }
    ]
    
    worker_df = pd.DataFrame(worker_data)
    expert_df = pd.DataFrame(expert_data)
    task_df = pd.DataFrame(task_metadata)
    
    logger.info(f"Loaded mock data: {len(worker_df)} worker responses, {len(expert_df)} expert ratings, {len(task_df)} tasks")
    
    return worker_df, expert_df, task_df


def prepare_analysis_data(worker_df: pd.DataFrame, expert_df: pd.DataFrame, task_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare combined dataset for analysis by joining the three datasets.
    
    Args:
        worker_df: Worker desire data
        expert_df: Expert ratings data  
        task_df: Task metadata
        
    Returns:
        Combined DataFrame ready for analysis
    """
    
    # Aggregate worker responses by task
    worker_summary = worker_df.groupby("Task ID").agg({
        "Automation Desire Rating": ["mean", "std", "count"],
        "Job Security Rating": "mean",
        "Enjoyment Rating": "mean",
        "Task": "first",
        "Occupation (O*NET-SOC Title)": "first",
        "Domain": "first"
    }).reset_index()
    
    # Flatten column names
    worker_summary.columns = [
        "Task ID", 
        "Automation Desire Rating",
        "Automation Desire Std",
        "Worker Count",
        "Job Security Rating", 
        "Enjoyment Rating",
        "Task",
        "Occupation",
        "Domain"
    ]
    
    # Aggregate expert ratings by task (in case multiple experts rate same task)
    expert_summary = expert_df.groupby("Task ID").agg({
        "Expert Capability Rating": "mean",
        "Confidence": "mean"
    }).reset_index()
    
    # Join datasets
    combined_df = worker_summary.merge(expert_summary, on="Task ID", how="left")
    combined_df = combined_df.merge(task_df[["Task ID", "O*NET-SOC Code", "Task Category"]], on="Task ID", how="left")
    
    # Calculate automation readiness (alignment between desire and capability)
    combined_df["Automation Readiness"] = combined_df.apply(
        lambda row: min(row["Automation Desire Rating"], row["Expert Capability Rating"]), 
        axis=1
    )
    
    # Calculate desire-capability gap
    combined_df["Desire Capability Gap"] = (
        combined_df["Automation Desire Rating"] - combined_df["Expert Capability Rating"]
    )
    
    return combined_df


def get_summary_stats(combined_df: pd.DataFrame) -> Dict:
    """Get summary statistics for the dashboard."""
    return {
        "total_tasks": len(combined_df),
        "total_workers": combined_df["Worker Count"].sum(),
        "avg_automation_desire": combined_df["Automation Desire Rating"].mean(),
        "avg_expert_capability": combined_df["Expert Capability Rating"].mean(),
        "avg_automation_readiness": combined_df["Automation Readiness"].mean(),
        "unique_occupations": combined_df["Occupation"].nunique(),
        "unique_domains": combined_df["Domain"].nunique()
    }