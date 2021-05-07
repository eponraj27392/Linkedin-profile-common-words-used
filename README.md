# Linkedin-profile-common-words-used

This repository help us to web scrap the LinkedIn profile and output the most common used by the profile.

Install all the necessary libraries using

```sh
pip install -r requirements.txt
```

if you encounter problems you may have to update pip first

```sh
python -m pip install --upgrade pip

```

Input your Login information in ``config.txt`` file in the below format.
```sh
username
password
```

## Preprocessing


A simple preprocessing class ``LinkedInScrapper`` from **webscrap.py** is created to scrap the given Linkedin url.

The preprocessed information had been converted to pandas DF format with all the activity information.
(Example, date posted, Likes, comment, subject, picture url, video inforamtion etc.,)

Later the text information had been preprocessed using  ``PreprocessText`` from **text_preprocess.py**  file where the frequency count of words used had been calculated.


## Web App using Dash 

I used Dash, from plotly, which helps us to develop web-based data visualization interfaces by putting together Plotly, React, and Flask.

For more information refer to [Dash](https://plotly.com/dash/)

For this analysis I made a simple web app, which takes input as
  
  *  --url          - which profile to be scrapped
  *  --period       - from which year the common words usage should be used for plotting
  *  --top_n_words  - how many Top N words to be displayed as a graph.
  
Run the below code in console after installed the necessary libraries,

```sh
python -m app -- url https://www.linkedin.com/in/satyanadella/ --period all --top_n_words 50
```   


**Run Dash App**


![DynamicPlottingImage](https://github.com/eponraj27392/Linkedin-profile-common-words-used/blob/master/start.gif)




**Dash App plot Results**

```sh
Consider this as a starting point for app/dashboard dev, many scrapped information can be analysed in detail which give us more information about the profile/url.
``` 

![DynamicPlottingImage](https://github.com/eponraj27392/Linkedin-profile-common-words-used/blob/master/final_gif.gif)






 

