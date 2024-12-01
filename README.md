[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/bt9dKHiK)
# W10 Summative

**AUTHOR:** Defne Ece Yavuz

**CANDIDATE NUMBER:** (THIS IS A 5-DIGIT NUMBER THAT LSE GIVES YOU EVERY YEAR. **DO NOT FORGET TO ADD THIS HERE.** IT IS IMPORTANT!)


![Cover image, male vs. female lyrics in pop songs](images/cover.jpg)


- [ ] Add a brief description of what this repository is about, what you wanted to discover when you started it and what you ended up doing/discovering
- [ ] Add instructions for how to recreate the Python environment for this project (either with pyenv or conda)
- [ ] Add instructions for how to obtain the Spotify API credentials and where to put them
- [ ] Add instructions for how to run the code to replicate the results

### Description
This repository is a summative assignment for the class DS105: Data for Data Science. 


Initially, my goal was to do an exploratory analysis of what defined "main pop girl" music - I wanted to get a list of top tracks by "main pop girls" such as Sabrina Carpenter, Chappel Roan, Olivia Rodrigo etc. and inspect their audio features. However, due to the deprecation of these endpoints in the Spotify API, I had to reformulate my research aim and question. 


### Research Question
What makes "main pop girl" music? What are its identifying qualities? How does it differ from other music (non-mainstream, non-pop, non-girl)?

### Aim

I will also aim to make predictions for two of the categories of the upcoming Grammy Music Awards

### Plan
1) Obtain top hits from 2000-2024
2) Obtain girly pop/"main pop girl" tracks
3) Combine these two playlists
4) Get top 5 female and male artists (decided through how many of their songs feature on the playlists)
5) Get these artists' top 10 tracks
6) Create a database of these songs
7) Get the lyrics to to these songs and put them in a database
8) Analyze these top 10 songs' lyrics to see whether they have any common themes or differences

### Table of Contents
| NB | Name | Content |
| :--: | :--- | :--- |
| 01 | Data Collection |  |
| 02 | Data Processing |  |
| 03 | Data Visualisation |  |

### How to recreate the Python environment


### How to obtain Spotify and Genius credentials and where to put them
To be able to run the code and obtain API data: 
1) Create an account or login to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and [Genius API page](https://genius.com/api-clients)
2) Create an app, name it (e.g., My App), describe it, and use the example Redirect URI link
3) Click on your My App Home and navigate to settings
4) Copy the Client ID and Client Secret 
5) Create a .env file and store the credentials there (as CLINET_ID and CLIENT_SECRET)
6) Install python-dotenv by running "pip install python-dotenv"
7) Import the .env file by running "From dotenv Import load_dotenv"



### How to Run the Code to replicate the results
