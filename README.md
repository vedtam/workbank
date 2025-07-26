# WORKBank Dashboard

**WORKBank** (AI Agent Worker Outlook and Readiness Knowledge Bank) is a comprehensive dashboard for exploring worker desire and technological capability of AI agents for occupational tasks across the U.S. workforce.

## Features

- **Overview Dashboard**: Key metrics and statistics from 1,500+ worker responses
- **Automation Desire Analysis**: Distribution analysis with filtering capabilities  
- **Automation Viability**: Scatter plot analysis of worker desire vs AI capability
- **Task Details**: Detailed analysis with sorting and filtering options
- **Data Export**: CSV download functionality for filtered datasets

## Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the dashboard:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Access the app:**
   Open your browser to http://localhost:8501

## Data Sources

The app integrates with three main WORKBank datasets from Hugging Face:

1. **Worker desire data**: `worker_data/domain_worker_desires.csv`
2. **Expert ratings data**: `expert_ratings/expert_rated_technological_capability.csv`
3. **Task metadata**: `task_data/task_statement_with_metadata.csv`

When internet access is available, the app automatically loads real data from the [SALT-NLP/WORKBank](https://huggingface.co/datasets/SALT-NLP/WORKBank) dataset. Otherwise, it uses structured mock data that matches the real schema.

## Dashboard Components

### Overview Tab
- Total tasks analyzed and workers surveyed
- Average automation desire and AI capability ratings
- Automation readiness metrics
- Unique occupations and domains covered

### Automation Desire Tab  
- Filter by domain and rating ranges
- Highest and lowest automation desire tasks
- Distribution histograms

### Automation Viability Tab
- Scatter plot of worker desire vs AI capability by domain
- Quadrant analysis for automation readiness
- Identification of automation-ready vs automation-wanted tasks

### Task Details Tab
- Sortable and filterable task list
- Detailed task information including O*NET codes
- Progress bars for all ratings
- Alignment indicators

### Data Export Tab
- Filter data by domain and occupation
- Preview filtered datasets
- CSV download functionality

## Architecture

- **`streamlit_app.py`**: Main dashboard interface with tabbed navigation
- **`data_loader.py`**: Data loading module with HuggingFace integration and fallback
- **`requirements.txt`**: Project dependencies

## About WORKBank

This database captures worker desire and technological capability of AI agents for occupational tasks, featuring preferences from 1,500 U.S. domain workers and capability assessments from AI experts across 844 tasks and 104 occupations.

**Resources:**
- 📄 [Read the paper](https://arxiv.org/abs/2506.06576)
- 🗃️ [Access dataset](https://huggingface.co/datasets/SALT-NLP/WORKBank)  
- 🌐 [Project website](https://futureofwork.saltlab.stanford.edu/)

## Data Analysis Code

- [automation_desire.ipynb](analysis/automation_desire.ipynb): Analysis of the distribution of automation desire ratings, analysis of the reason behind automation desire.
- [automation_viability.ipynb](analysis/automation_viability.ipynb): Analysis of the automation desire-capability landscape.
- [human_agency_scale.ipynb](analysis/human_agency_scale.ipynb): Analysis of the worker-desired human agency level and the expert-assessed feasible human agency level for different tasks.
- [human_skill_shift.ipynb](analysis/human_skill_shift.ipynb): Analysis of demographic and occupational coverage of WORKBank and mixed-effects model regression on worker responses.

## Want to Launch the Audit in Your Organization?

Unlike traditional surveys, our auditing framework features an audio-enhanced interface and combines quantitative ratings with analysis of audio transcripts. This approach enables more calibrated and context-rich responses. We are also working to support input from additional modalities.

**If you're interested in deploying the audit to explore the future of work within your organization, feel free to fill out [the interest form](https://forms.gle/hFGyhYkD1VwMLVj59).**


## Citation

Please cite our paper if you use WORKBank database or analysis code in your work:

```
@misc{shao2025futureworkaiagents,
      title={Future of Work with AI Agents: Auditing Automation and Augmentation Potential across the U.S. Workforce}, 
      author={Yijia Shao and Humishka Zope and Yucheng Jiang and Jiaxin Pei and David Nguyen and Erik Brynjolfsson and Diyi Yang},
      year={2025},
      eprint={2506.06576},
      archivePrefix={arXiv},
      primaryClass={cs.CY},
      url={https://arxiv.org/abs/2506.06576}, 
}
```

## Data Analysis Code

- [automation_desire.ipynb](analysis/automation_desire.ipynb): Analysis of the distribution of automation desire ratings, analysis of the reason behind automation desire.
- [automation_viability.ipynb](analysis/automation_viability.ipynb): Analysis of the automation desire-capability landscape.
- [human_agency_scale.ipynb](analysis/human_agency_scale.ipynb): Analysis of the worker-desired human agency level and the expert-assessed feasible human agency level for different tasks.
- [human_skill_shift.ipynb](analysis/human_skill_shift.ipynb): Analysis of demographic and occupational coverage of WORKBank and mixed-effects model regression on worker responses.

## Want to Launch the Audit in Your Organization?

Unlike traditional surveys, our auditing framework features an audio-enhanced interface and combines quantitative ratings with analysis of audio transcripts. This approach enables more calibrated and context-rich responses. We are also working to support input from additional modalities.

**If you're interested in deploying the audit to explore the future of work within your organization, feel free to fill out [the interest form](https://forms.gle/hFGyhYkD1VwMLVj59).**


## Citation

Please cite our paper if you use WORKBank database or analysis code in your work:

```
@misc{shao2025futureworkaiagents,
      title={Future of Work with AI Agents: Auditing Automation and Augmentation Potential across the U.S. Workforce}, 
      author={Yijia Shao and Humishka Zope and Yucheng Jiang and Jiaxin Pei and David Nguyen and Erik Brynjolfsson and Diyi Yang},
      year={2025},
      eprint={2506.06576},
      archivePrefix={arXiv},
      primaryClass={cs.CY},
      url={https://arxiv.org/abs/2506.06576}, 
}
```
