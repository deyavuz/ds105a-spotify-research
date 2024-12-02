[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/bt9dKHiK)
# W10 Summative

**AUTHOR:** Defne Ece Yavuz

**CANDIDATE NUMBER:** 37492

![Cover image, male vs. female lyrics in pop songs](images/cover.jpg)
Image credit: ChatGPT

### 🎸 Description
This repository is a summative assignment for the class DS105: Data for Data Science. Through this repository, I will be using data gathered mainly through the Spotify API, and supplemented by the Genius API, to investigate how pop songs by male vs. female musical artists differ.

Initially, my goal was to do an exploratory analysis of what defined "main pop girl" music - I wanted to get a list of top tracks by "main pop girls" such as Sabrina Carpenter, Chappel Roan, Olivia Rodrigo etc. and inspect their audio features. However, due to the deprecation of these endpoints in the Spotify API, I had to reformulate my research aim and question. 

So, I ended up gathering data through two Spotify user-created playlists, "Pop Hits 2000s - 2024", to see which artists featured most over 2000-2024 in top pop hits tracks, and "girly pop songs", to diversify and reduce bias in the dataset, as due to recent API restrictions I couldn't use Spotify-created playlists and I wanted to get an unbiased, unopinionated sense of "top hits". So, I obtained data through two user-created playlists with different vibes/aesthetics and focal time periods (pop hits with a wider time range and girly pop songs with a focus on contemporary pop).

### 🎻 Background/Literature Review
[This extended abstract](https://comma.eecs.qmul.ac.uk/assets/pdf/vjosa_IC2S2_23.pdf) by Preniqi et al. (2023) suggests that love is a more common theme with female artists compared to male. Additionally, male artists are more likely to write and sing about sexist and gender biased topics, including descriptions of "vulgarity and dominance", especially post-90s (i.e., our dataset), while female artists tended to write on more self-introspective topics. The findings showed that female artists had more positive sentiments in their lyrics, while the negative sentiments were equal for both genders. The abstract did not expand upon compunded values, but it can be inferred that female artists had overall more positive sentiments in their lyrics. 

[This exploratory analysis](https://www.storybench.org/analyzing-gender-differences-in-music-themes-and-lyrics/) by Samuel Chan found that male artists were more likely to use negative words and phrases when talking about their breakup/exes, while female artists used negative and positive words equally. 

Looking at these two studies, I am predicting that women will have a higher (more positive) compounded sentiment, compared to male artists. 

### 🥁 Research Question
Is there a difference between top pop hits by male and female musical artists?

### 🎹 Variables
I have decided to operationalize "differences" in top pop hits by using the Genius API and supplementing my research by looking at song lyrics and performing sentiment analysis using Natural Language Toolkit (NLTK) and its built-in [VADER lexicon](https://github.com/cjhutto/vaderSentiment), which is great for such task because it is specialised in understanding social media-speak and complex sentiments, which is prevalent in modern-day pop music. 

So, my variables are as follows:

**Independent variable:** Song lyrics of top 10 songs of top artists
**Dependent variables:** Lyrics sentiment compound values (from -1 to 1)

### 🎺 Hypothesis
Based on my brief literature review, I am predicting that:
**H0:** There won't be any differences in themes between top pop hits by male and female artists.
**H1:** Songs by female musical artists will have a higher compounded sentiment (indicating an overall more positive sentiment), compared to songs by male artists.

### 🎵 Methodology
1) Obtain top hits from 2000-2024
2) Obtain girly pop/"main pop girl" tracks
3) Combine these two playlists, create a dataframe
4) Get top 5 female and male artists (decided through how many of their songs feature on the playlists)
5) Get these artists' top 10 tracks
6) Create a dataframe of these songs
7) Get the lyrics to to these songs and add them to the dataframe
8) Create a SQL database, with the foreign key "Artists"
9) Analyze these songs' lyrics through sentiment analysis to see their sentiments
10) Compare the genders' lyrical sentiments and plot them!

### 🎷 Table of Contents
| NB | Name | Content |
| :--: | :--- | :--- |
| 01 | [Data Collection](../code/NB01-Data-Collection.ipynb) |  |
| 02 | [Data Processing](../code/NB02-Data-Processing.ipynb) |  |
| 03 | [Data Visualisation](../code/NB03-Data-Visualisation.ipynb) |  |

### 🪕 How to recreate the Python environment
1) Install pyenv through running `brew install pyenv` (for Mac) `or curl https://pyenv.run | bash` (for Linux)
2) Install the required Python version by running `pyenv install 3.12.2` and then `pyenv local 3.12.2`
3) To create and activate the virtual environment, run `python -m venv venv` and then `source venv/bin/activate` (for Mac/Linux) and `.\venv\Scripts\activate` (for Windows)
4) Run pip install -r requirements.txt, where requirements.txt is a document containing all the required libraries (e.g., pandas) and the versions to be used

### 🎶 How to obtain Spotify and Genius credentials and where to put them
To be able to run the code and obtain API data: 
1) Create an account or login to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and [Genius API page](https://genius.com/api-clients)
2) Create an app, name it (e.g., My App), describe it, and use the example Redirect URI link
3) Click on your My App Home and navigate to settings
4) Copy the **Client ID** and **Client Secret**
5) Create a .env file and store the credentials there (as **CLINET_ID** and **CLIENT_SECRET**) - these should always be hidden, so do not push onto Git or share publicly
6) Install python-dotenv by running `pip install python-dotenv`
7) Import the .env file by running `From dotenv Import load_dotenv`
8) Write a get_token() function in a separate file, auth.py, to streamline access token calling and using. Import the function through `From auth.py Import *` and utilize when calling endpoints

### 🪗 How to run the code to replicate the results
To run the code as intended (to replicate the results):
1) Install the required dependencies by running `pip install -r requirements.txt`
2) Activate the Python environment, as described above, by running `source venv/bin/activate`
3) Run the Notebooks, starting from NB01, then NB02, and finally NB03
