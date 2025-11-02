
# 💻 Interview Prep Data Collection & Analysis

### ✨ Description
An automation script to scrape text content from a list of external links (initially planned for YouTube transcripts but pivoted to general web pages) in an Excel file and automatically upload the compiled JSON file to Google Drive.

### 🌟 Project Background & Motivation
The process of preparing for interviews often involves significant manual effort in searching, collecting, and organizing relevant questions and answers. 
This project was initiated to streamline and automate this time-consuming information-gathering process, allowing users to quickly compile a rich repository of study materials.

Initially, the goal was to extract YouTube video transcripts to build a comprehensive knowledge base. 
However, due to persistent API-related blocking issues (Error code 403) and time constraints (which resulted in spending nearly a day troubleshooting), the project was re-scoped to general web page content scraping for link-based text retrieval.

### 🚀 Features & Outcomes
- Excel File Processing: Automatically reads links from a specified Excel spreadsheet.
- Web Scraping: Crawls each link to extract all available text content.
- JSON Compilation: Consolidates all scraped text into a single, organized JSON file.
- Google Drive Integration: Utilizes the Google Cloud Console API for secure and automated file upload to a designated Google Drive folder.
- Batch Automation: A dedicated batch file bundles the scraping and upload processes into a single, seamless execution.
