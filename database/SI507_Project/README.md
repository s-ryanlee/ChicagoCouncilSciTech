# SI507 - Intermediate Programming Final Project
[Course Listing](https://www.si.umich.edu/programs/courses/507/)

# Final Project Overview

## Milestones

There are 3 milestones that need to be turned in.
1. Project Proposal, due April 2
2. Data Checkpoint & Interactive Presentation Design, due April 19
3. Final Project Demo and Repository Link Submission, due April 28 (keep in mindthis is during finals week)

The goal of the final project is for you to showcase what you’ve learned in 507 regarding:
- Accessing data via web APIs, including those that require authentication
- Accessing data via scraping
- Accessing data efficiently and responsibly using cachingUsing a database to store and access relational data
- Use basic python data structures and operations to analyze and process data in“interesting” ways
- Use a presentation tool or framework to present data to a user
- Support basic interactivity by allowinga user to choose among different datapresentation options

## Here are a couple of examples that would be reasonable final projects:
- A program that lets a user choose a city and see the average ratings for differentrestaurant types(e.g., bar, breakfast, Indian, Mediterranean) from Google, Yelp,and OpenTable as plotly bar or scatter charts.
- A program that aggregates crime data fromhttps://spotcrime.com/mi/ann+arbor/daily and allows a user to select one ormore crime types to see a graph of crime frequency by month, either for a singleyear comparing across several years.


# Project Proposal and Checklist

## Data Sources

### Data Origin: [c2st.org/events](https://www.c2st.org/events)

### Data Access

I used the requests module to access the data, Beautiful Soup to parse html, and have plans to implement caching functions similar to the implemenation in [Project 2](https://github.com/s-ryanlee/Project2Winter2021). 

### Summary of Records

- Estimated Total Records
    - There are about 5 events per Event listing page
    - There are 53 pages of events
    - Estimated 265 records to be compiled
- Current Records:
    - Currently I've compiled 5 records and working on a function to crawl each of the event listing pages to collect the reamining ~260 records

## Database

Events are the primary linking source available. Web traffic data is collected by the organization from Google Analytics and reported on monthly via Google Data Studio.
Eventbrite event registration pages, c2st.org event specific pages, and YouTube videos are all linked through each specific C2ST event. 
Additional data that is tracked includes analytics from Facebook and Event attendance are exported and entered manually, respectively.
