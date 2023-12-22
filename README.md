# Review Summarizer AI

## 📖 Introduction
Review Summarizer AI is a web application designed to efficiently scrape and summarize user reviews from Google Maps locations. It uses Python, FastAPI, and modern web technologies to provide real-time, insightful summaries, aiding users in making informed decisions based on collective reviews.


## 🛠️ Installation
To set up the project, follow these steps:

### Requirements:
- Python 3.6 or higher
- FastAPI
- Pyppeteer
- uvicorn
- Google generative Ai(API Key)

### Setup:
```bash
git clone [repository-url]
pip run config.py
```


## 👨‍🏫 Get Started
To get the application running:
- Start the FastAPI server:
```bash
uvicorn app:app --reload
```
- Open your web browser and navigate to:
http://127.0.0.1:8000/
- Enter a url from google maps.

## 📘System Overview
- Backend: Python and FastAPI handle server-side operations, including routing, request handling, and running the main application logic.
- Web Scraping: pyppeteer is used for dynamic web scraping, targeting user reviews from specified Google Maps locations.
- Summarization: Implements a model (e.g., Google's PALM model) for generating concise summaries from the collected reviews.
- Frontend: HTML/CSS/JS used to create responsive user interface for users to interact with the application, input URLs, and display the summarized results.
- Api: Google generative ai.[link](https://ai.google.dev/)

## 💻 Code Walkthrough
### APP.PY:
Contains the main FastAPI application setup, routes, and server logic.
#### Imports and Initial Setup: 
Import necessary libraries for the web app, including FastAPI for the web framework, HTTPException for error handling, and the scrape and summarize functions from a local module. It initializes the FastAPI application.
```
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles

from summarize import scrape_reviews, summarize
import google.generativeai as palm
import config

app = FastAPI()
```
#### PALM Configuration:
Configure the Google Generative AI (PALM) using the API key from the config module and select a suitable model(PALM) from those available that support text generation.
```
palm.configure(api_key=config.API_KEY)
models = [m for m in palm.list_models() if "generateText" in m.supported_generation_methods]
model = models[0].name
```
#### FastAPI Endpoint:'/scrape-and-summarize/'
- Endpoint: A POST endpoint /scrape-and-summarize/ that accepts a request with a URL.
- Request Handling: The function reads the JSON body of the request to extract the URL.
- Scraping and Summarizing: Uses the scrape_reviews function to scrape reviews from the URL and then passes the collected reviews to the summarize function for summarization.
- Error Handling: Includes error handling for missing URLs and any exceptions during the scraping and summarizing process.
```
@app.post("/scrape-and-summarize/")
async def scrape_and_summarize(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=422, detail="URL is required")
    try:
        reviews = await scrape_reviews(url)
        summary = summarize(reviews, model)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```
#### Serving Static Files:
Mounts a directory as a static files location, allowing FastAPI to serve HTML, CSS, and JavaScript files necessary for the web application's user interface.
```
app.mount("/", StaticFiles(directory=".", html=True), name="static")
```

### SUMMARISE.PY:
Defines the functions for scraping and summarizing reviews using pyppeteer and the PALM model.
#### Imports and Configuration
- google.generativeai (as palm): Imports Google's generative AI, presumably to use its text generation capabilities for summarizing the reviews.
- asyncio: This is used for writing concurrent code using the async/await syntax, necessary for the asynchronous execution of the web scraping and possibly for the AI summarization.
- pyppeteer: A Python library for controlling headless Chrome or Chromium, used here for web scraping.
- config: A custom module,containing configuration variables like API keys, and necessary libraries.
```
import google.generativeai as palm
import asyncio
from pyppeteer import launch
import config

palm.configure(api_key=config.API_KEY)
models = [m for m in palm.list_models() if "generateText" in m.supported_generation_methods]
model = models[0].name
```


#### Asynchronous Function: scrape_reviews(url)
This function is the core of the web scraping process.
```
async def scrape_reviews(url):
    reviews = []
    # Browser setup and navigation code
    # ...
    return reviews

```

- Browser Setup: It launches a headless browser with specific dimensions using pyppeteer.
- Page Navigation: Opens a new page and navigates to the provided URL.
```
browser = await launch({"headless": True, "args": ["--window-size=800,3200"]})
page = await browser.newPage()
await page.setViewport({"width": 800, "height": 3200})
await page.goto(url)
await page.waitForSelector(".jftiEf")
```
- Content Scraping: Waits for specific elements (identified by CSS selectors) to load on the page. It then iterates over these elements, extracting text.
- Handling More Buttons: Some reviews might be partially hidden and require clicking a button to read entirely. The function tries to find and click these buttons to reveal the full reviews.
```
elements = await page.querySelectorAll(".jftiEf")
for element in elements:
    try:
        await page.waitForSelector(".w8nwRe")
        more_btn = await element.querySelector(".w8nwRe")
        await page.evaluate("button => button.click()", more_btn)
        await page.waitFor(5000)
    except:
        pass
```
- Extracting and Storing Reviews: Extracts text from each review element and appends it to a list of reviews.
- Closing Browser: Once all reviews are scraped, it closes the browser and returns the list of reviews.
```
snippet = await element.querySelector(".MyEned")
text = await page.evaluate("selected => selected.textContent", snippet)
reviews.append(text)
await browser.close()
```
#### Function: summarize(reviews, model)
This function takes the scraped reviews and uses the PALM model to generate a summary.
```
def summarize(reviews, model):
    prompt = "I collected some reviews of a place I was considering visiting. \
    After going through the reviews, break it down into pros and cons. Also give me a final decision whether i should visit or not.\n"
    for review in reviews:
        prompt += "\n" + review
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        max_output_tokens=300,
    )
    return completion.result
```

- Prompt Creation: Constructs a prompt string by appending each review. This prompt instructs the model to break down the reviews into pros and cons and make a final decision about visiting the place.
```
prompt = "I collected some reviews of a place I was considering visiting. \
After going through the reviews, break it down into pros and cons. Also give me a final decision whether i should visit or not.\n"
for review in reviews:
    prompt += "\n" + review
```
- Model Invocation: Calls the PALM model with the constructed prompt and other parameters like temperature and max output tokens to control the generation.
```
completion = palm.generate_text(
    model=model,
    prompt=prompt,
    temperature=0,
    max_output_tokens=300,
)
```
- Returning Result: Returns the generated text, which is the summary of reviews.
```
return completion.result
```
#### Configuration and Model Selection
  Configuring the PALM library using an API key from the config module and selecting a model from the available ones that support text generation.```
```
palm.configure(api_key=config.API_KEY)
models = [m for m in palm.list_models() if "generateText" in m.supported_generation_methods]
model = models[0].name
```

### INDEX.HTML: 
The main HTML file for the web application's user interface.
### STYLE.CSS: 
Contains all styling for the web application to ensure a consistent and responsive user interface.
### SCRIPT.JS: 
Includes JavaScript code for handling user interactions, making requests to the server, and updating the UI with response data.
#### Event Listener Attachment
```
document.getElementById('urlForm').addEventListener('submit', async function(e) {
    //...
});
```
- Event Listener: Attaches an event listener to the form identified by 'urlForm'. The listener triggers on the 'submit' event, which occurs when the form is submitted.
- Async Function: The function handling the event is asynchronous (async), indicating that it will perform asynchronous operations inside, specifically network requests.
#### Prevent Default Form Behavior
````
e.preventDefault();
````
Prevents the form's default submission behavior, which typically causes a page reload. This allows the script to handle submission using AJAX for a smoother user experience.
#### Retrieving URL from the Form
```
const url = document.getElementById('urlInput').value;
```
Gets the value entered in the input field (presumably where users enter the URL for the reviews they want summarized) identified by 'urlInput'.
#### Sending Request to Server
```
const response = await fetch('/scrape-and-summarize/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url: url })  // Ensure this matches the expected format
});
```
- Fetch API: Uses the fetch API to send a POST request to the /scrape-and-summarize/ endpoint.
- Headers: Includes headers to indicate that the payload is JSON.
- Body: The body of the request is a JSON string containing the URL fetched from the form.
#### Handling Response
```
const result = await response.json();
```
Waits for the server to respond and converts the response to a JSON object, which is expected to contain the summary data.
#### Displaying the Summary
```
document.getElementById('summaryOutput').innerText = result.summary || "No summary available";
```
 Updates the text of the element identified by 'summaryOutput' with the summary returned from the server. If no summary is returned (perhaps due to an error or no reviews being found), it falls back to displaying "No summary available".

## 🌟 Project Impact
In today's fast-paced world, individuals often rely on reviews to make informed decisions about where to dine, travel, or shop. However, the sheer volume of user-generated reviews can be overwhelming, making it challenging to sift through each one to gauge overall sentiment. The Review Summarizer AI steps in as an innovative solution, condensing and synthesizing vast numbers of reviews into concise, insightful summaries. This application empowers users by providing a quick, comprehensive understanding of public opinion, thus saving valuable time and aiding in making confident, informed decisions. Whether it's choosing the next culinary adventure, selecting a travel destination, or planning an outing, the Review Summarizer AI ensures that the best choices are just a summary away.

 ## 🎥 Video Demonstration
 Check out the video demonstration [here](https://drive.google.com/file/d/12faxIP0d0gIP8yWJBm_i1NMw3xRbnQyQ/view?usp=sharing) to see the Review Summarizer AI in action! 
