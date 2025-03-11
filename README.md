# ai-news-generator

## **Functional Requirements**  

- **Scraping and Content Generation:**  
  - A module that performs scraping from specified news sources.  
  - A content generation function that, using an LLM, processes the extracted information and generates a daily summary.  
  - A periodic task that calls this function and stores the result in the database.  

- **URL Management:**  
  - A routing system that associates each generated summary with a date-based URL.  
  - Example: The `/22102024` route will return the summary generated for October 22, 2024.  

- **Newsletter:**  
  - An integration module to send a daily email with the generated summary.  
  - Ability to add and remove users from the newsletter.