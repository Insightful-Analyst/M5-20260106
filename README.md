# M5-20260106

# **Library Data ETL Project**
## Scenario  
A library wants to improve their current quality analysis, as manually completing the task takes too much time and is less reliable. They are looking for a more efficient way to filter data using Python and automation. They have heard of a tool called Azure DevOps and want to apply it to their process.

## Task 
Using the knowledge learnt over the past few modules, design and create a project that uses and manipulates data and puts it into another location ready for presentation purposes. Your project will include: 
* Documenting architecture design, testing plans and agile kanban for 
planning.  
* Setting up an agile Kanban board to use for planning.  
* Storing code result in a central GitHub Repository.  
* Using data provided to manipulate and clean up the results ready for the next stage using Python tools.  
* Testing the application with unit testing.  
* Using a CI/CD pipeline to automate the data transformation process.  
* Reporting security practices that can be applied to the project.  
 
## Objectives  
- The architecture design.  
- A demonstration of the pipeline and application working.  
- A talk through the PowerBi infographics.


## Architecture Diagram
<img width="616" height="382" alt="image" src="https://github.com/user-attachments/assets/3bf3c9e5-fe84-4d4e-b300-70d1815fb251" />

## User Stories
- As a Library Manager, I want to receive automated, reliable reports on our collection and circulation data quality,
So that I can make informed decisions about resource allocation, identify trends in patron behavior, and ensure our catalog accuracy without depending on manual data checks.

- As a Data Analyst, I want to generate infographics using Power BI so that the data can be presented visually to stakeholders.

- As a Librarian/User, I want to be able to lookup book statuses, customer details etc.

- As a Data Engineer, I want to validate the data transformation process with end-to-end testing to ensure data integrity is maintained throughout the pipeline.

- As a data engineer, I want to build an automated solution that cleans and validates the library data. So that I can provide stakeholders with library metrics.

- As a data engineer, I want to build a monitoring dashboard. So that I can view the results of my automated pipeline.

- As a Stakeholder, I want to have a clear documentation of the architecture design, so that I can understand the structure and flow of the ETL process.

## Project Progress

- The jupiter notebook created to transform the library's raw daya was converted into a python file.
- The script was enhanched by adding functions, an enriched date colum, and loading the result table into a sql database.
- A unit test file was created to test the enriched_dateDuration calculation (the test was done on the python file created by the tutor and stored in the solutions_nirosh folder)

## Requirements Update
Library now wants their customers need to able to log in and be able to see data relevant to them.
I need a proposed solution/ architecture diagram.

Create an architecture diagram for new requirement:
- User must be able to log in and see data about their library usage.
- This must be a simple, low budget POC but production grade.

## Updated Architecture Diagram
