<p align="center">
<img src="assets/workbank-text.svg" style="width: 40%; height:auto" />
</p>
<h3 align="center">
<p>Large-scale audit of worker desire and technological capability of AI agents for work
</h3>
<p align="center">
| <a href="https://arxiv.org/abs/2506.06576"><b>Paper</b></a> | <a href="https://futureofwork.saltlab.stanford.edu/"><b>Website</b></a> | <a href="https://huggingface.co/datasets/SALT-NLP/WORKBank"><b>HF Dataset</b></a> |
</p>
<img src="assets/workbank.png" style="width: 100%; height: auto" />

**Latest News** 🔥
- [2025/07] Our project is featured by <a href="https://hai.stanford.edu/news/what-workers-really-want-from-artificial-intelligence">Stanford HAI</a> and <a href="https://www.forbes.com/sites/moinroberts-islam/2025/06/30/future-of-work-41-of-ai-startups-build-automation-workers-dont-want/">Forbes</a> - check out the coverage!

## Overview

**WORKBank** (AI Agent Worker Outlook and Readiness Knowledge Bank) is a database that captures worker desire and technological capability of AI agents for occupational tasks.

The current version of WORKBank includes preferences from 1,500 U.S. domain workers and capability assessments from AI experts, covering over 844 tasks across 104 occupations collected between January and May 2025. This database stems from our project detailed in [Future of Work with AI Agents: Auditing Automation and Augmentation Potential across the U.S. Workforce](https://arxiv.org/abs/2506.06576) that introduces a novel auditing framework to assess which occupational tasks workers want AI agents to automate or augment, and how those desires align with the current technological capabilities.

## Database Access

We host our database on Hugging Face.  All variables are documented and explained in the [Code Book](codebook.pdf).

To download our database, run:

```python
from datasets import load_dataset


worker_desire = load_dataset("SALT-NLP/WORKBank", data_files="worker_data/domain_worker_desires.csv")["train"]

expert_ratings = load_dataset("SALT-NLP/WORKBank", data_files="expert_ratings/expert_rated_technological_capability.csv")["train"]

task_meta_data = load_dataset("SALT-NLP/WORKBank", data_files="task_data/task_statement_with_metadata.csv")["train"]
```

You can also manually download the CSV files [here](https://huggingface.co/datasets/SALT-NLP/WORKBank/tree/main).

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
