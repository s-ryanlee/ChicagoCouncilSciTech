# Current Data Organization Methods and Data Organization Best Practices

Prepared for C2ST by Samantha Ryan-Lee

**From Broman, Karl W, & Woo, Kara H. (2018). Data Organization in Spreadsheets. The American statistician, 72(1), 2–10.**

## Background
> "Spreadsheets are often used as a multipurpose tool for data entry, storage, analysis, and visualization. 
> Most spreadsheet programs allow users to perform all of these tasks, however we believe that spreadsheets are best suited to data entry and storage, and that analysis and visualization should happen separately."
>
> "Analyzing and visualizing data in a separate program, or at least in a separate copy of the data file, reduces the risk of contaminating or destroying the raw data in the spreadsheet."

C2ST uses a combination of Google Analytics, Facebook Business Page Analytic Reporting, Conferences I/O, and Google Forms to collect their data. 
Google Data Studio is used to automatically generate monthly reports that measure web traffic across their primary website (c2st.org) and their event registration website (eventbrite.com), as well as YouTube video views and watchtimes.
Monthly reports and data are not currently collected and stored, as Data Studio enables users to view data and reports for any given date range.

![Monthly Data Studio Report for c2st.org](https://github.com/s-ryanlee/ChicagoCouncilSciTech/blob/f9e515b7217a2677c483fb808e0190fbcb28ba22/assets/data_practices/data_studio_monthly_example.PNG)

C2ST currently utilizes Conferences I/O to manage the surveys that collect audience feedback for each of their programs.
Excel documents are exported from this platform, and contain two sheets: generalized summary of responses (including the relative frequencies of responses and sums for each response), and a table of each response that also includes descriptive statistics for each survey question.

![Conferences I/O Generalized Summary of Responses](https://github.com/s-ryanlee/ChicagoCouncilSciTech/blob/f9e515b7217a2677c483fb808e0190fbcb28ba22/assets/data_practices/conferences_io_summary.PNG)

![Conferences I/O Individual Responses with Descriptive Statistics](https://github.com/s-ryanlee/ChicagoCouncilSciTech/blob/8ba43a02abe35211ad7d61b0967775cc453ef8c5/assets/data_practices/conferences_io_responses.PNG)

## Data Organization Best Practices

The following sections review specific recommendations from Broman & Woo (2018) regarding data organization and storage in spreadsheets.

### Consistency

> "Entering and organizing your data in a consistent way from the start will prevent you and your collaborators from having to spend time harmonizing the data later."
> - "Use consistent codes for categorical variables"
> - "Use a consistent fixed code for any missing values"
> - "Use consistent variable names."
> - "Use consistent subject identifiers."
> - "Use a consistent format for all dates, preferably with the standard format YYYY-MM-DD."
> - Use consistent phrases in your notes.
> - Be careful about extra spaces within cells (leading/trailing spaces)

### Naming Conventions

> "Choose good names for things."
> - "No spaces (in variable and file names)." 
> - "Caution with leading/trailing spaces."
> - "Avoid special characters."
> - "Use short but meaningful names."
> - "Avoid using 'final'."

!["Data Organization in Sheets" Table 1](https://github.com/s-ryanlee/ChicagoCouncilSciTech/blob/f9e515b7217a2677c483fb808e0190fbcb28ba22/assets/data_practices/data_organization_in_sheets.PNG)

### Empty Cells and Avoid Many Things in One Cell
> "Use common codes for missing data."
> 
> "Only one thing in each cell. Each cell should contain one piece of data."

![Data Manipulation Flow](https://github.com/s-ryanlee/ChicagoCouncilSciTech/blob/d84c81179a447d52d136cd28bcf476c0150e2826/assets/data_practices/better_formatting_flow.png)

### Data Dictionaries
> "Have a separate file that explains what all the variables are."
> 
> Might contain:
> - "Exact variable name as it appears in the data file."
> - "A version of the variable name that might be used in data visualizations."
> - "A longer explanation of what the variable means."
> - "The measurement units."
> - "Expected minimum and maximum values (or formatting)."

### No Calcuations in Raw Data Files
> "Primary data files should be a pristine store of data. Write-protect it, back it up, and do not touch it."
> 
> "If you want to do some analyses in Excel, make a copy of the file and do your calcuations and graphs in the copy."



