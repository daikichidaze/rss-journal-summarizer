### Integrated README for Python Project

#### Project Description

This project is designed to automatically retrieve, summarize, and send summaries of recent entries from international organizations to a designated Slack channel. It integrates with OpenAI's API to generate concise summaries and uses a Slack webhook to notify team members. The project consists of several Python scripts each handling specific parts of the process.

#### Components

1. **main.py**: The main script that orchestrates the workflow of retrieving entries, summarizing abstracts, and sending notifications.
2. **retriever.py**: Manages the fetching of recent entries from an RSS feed and extracts abstracts.
3. **openai_wrapper.py**: Interfaces with OpenAI's API to summarize the abstracts using a structured prompt.
4. **sender.py**: Handles the sending of formatted messages to a Slack channel using a webhook.

#### Workflow

- The script initializes in the Indochina Timezone (ICT).
- Reads necessary credentials from environment variables.
- Retrieves entries from the last 62 days and processes them for summarization.
- Sends formatted summaries to a Slack channel, pausing briefly between posts to manage API usage.

#### Environment Variables

- `OPENAI_API_KEY`: Required for accessing OpenAI's API services.
- `SLACK_URL`: The Slack webhook URL for sending notifications.

#### Dependencies

- Python libraries: `json`, `os`, `datetime`, `time`, `pytz`, `feedparser`, `requests`, `BeautifulSoup`
- External libraries: `openai`, `requests`

#### Installation

Ensure all Python dependencies are installed. For external libraries, use:

```bash
pip install feedparser requests beautifulsoup4 pytz openai
```

#### Usage

Ensure environment variables are set up correctly. Run the project with:

```bash
python main.py
```

Check the specified Slack channel for incoming summaries.

#### Detailed Usage and Configuration

1. **Retrieving and Processing Entries**:

   ```python
   from retriever import InternationalOrganizationRetriever
   retriever = InternationalOrganizationRetriever()
   recent_entries = retriever.fetch_recent_entries(now, hours_ago=24)
   ```

2. **Summarizing Abstracts**:

   ```python
   from openai_wrapper import summarize_abstract
   summary = summarize_abstract(abstract, api_key)
   ```

3. **Sending to Slack**:
   ```python
   from sender import SlackSender
   sender = SlackSender(webhook_url)
   sender.send_summary(entry, summary, journal_title)
   ```

#### Note

This integrated approach reduces redundancy in module descriptions, focusing on how each part contributes to the overall functionality of the project, making it clear and concise for users to understand and implement.
