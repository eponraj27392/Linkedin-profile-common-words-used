# -*- coding: utf-8 -*-
"""
Created on Tue May  4 21:40:25 2021
@author: eponr
Information related to web scrapping
source code : https://christophegaron.com/scraping-linkedin-posts-with-selenium-and-beautiful-soup/
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup as bs

import re
import time
import glob
import argparse
import pandas as pd
import numpy as np
import datetime
from datetime import date
from utils import *
from text_preprocess import *
import plotly.graph_objects as go
from plotly.offline import plot


class LinkedInScrapper:
    def __init__(self, period = 'all', url = None, top_n = None):
        self.url                     = url
        self.period                  = str(period) + '-01-01' if period != 'all' else 'all'
        self.top_n_words             = int(top_n)
        self.username, self.password = self.read_configs('config.txt')
        self.post_dates              = []
        self.post_texts              = []
        self.post_likes              = []
        self.post_comments           = []
        self.video_views             = []
        self.media_links             = []
        self.media_type              = []
        self.comment_count           = []
        
        if self.url.split('/')[3] == 'company':
             self.user_name = self.url[33:-1]
             self.post_link = 'posts/'
        else:
            self.user_name  = self.url[28:-1]
            self.post_link  = 'detail/recent-activity/shares/'


        self.driver  = webdriver.Chrome(str(PROJECT_DIR) + '\\chromedriver.exe')
        self.driver.get('https://www.linkedin.com/uas/login')
        
        self.element = self.driver.find_element_by_id('username')
        self.element.send_keys(self.username)
        self.element = self.driver.find_element_by_id('password')
        self.element.send_keys(self.password)
        self.element.submit()
        

    
    def read_configs(self, file_name):
        config_file  = open(str(PROJECT_DIR) + '\\' + file_name)
        lines        = config_file.readlines()
        try:
            username = lines[0]
            password = lines[1]
            return username, password
        except:
            raise print('Input the confidential attributes inside the file')
            
        
    def scrap_url(self):
        self.driver.get(self.url +  self.post_link)  
        final_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == final_height:
                print(final_height)
                print(new_height)
                break
            final_height = new_height
                
        company_page      = self.driver.page_source  
        linkedin_soup     = bs(company_page.encode("utf-8"), "html")
        linkedin_soup.prettify()
        scrap_source_data = linkedin_soup.findAll("div",{"class":"occludable-update ember-view"})
        
        return scrap_source_data

    
    def scrap_req_info(self, scraped_data):
        
        #Looping through the posts and appending them to the lists
        for single_post in scraped_data:
            
            try:
                posted_date = single_post.findAll("span",{"class":"visually-hidden"})
                text_box = single_post.find("div",{"class":"feed-shared-update-v2__description-wrapper ember-view"})
                text = text_box.find("span",{"dir":"ltr"})
                new_likes = single_post.findAll("li", {"class":"social-details-social-counts__reactions social-details-social-counts__item"})
                new_comments = single_post.findAll("li", {"class": "social-details-social-counts__comments social-details-social-counts__item"})
        
                #Appending date and text to lists
                self.post_dates.append([i.text.strip() for i in posted_date if 'ago' in i.text.strip()][0])
                self.post_texts.append(text_box.text.strip())
        
        
                try:
                    video_box = single_post.findAll("div",{"class": "feed-shared-update-v2__content feed-shared-linkedin-video ember-view"})
                    video_link = video_box[0].find("video", {"class":"vjs-tech"})
                    self.media_links.append(video_link['src'])
                    self.media_type.append("Video")
                except:
                    try:
                        image_box = single_post.findAll("div",{"class": "feed-shared-image__single_post"})
                        image_link = image_box[0].find("img", {"class":"ivm-view-attr__img--centered feed-shared-image__image feed-shared-image__image--constrained lazy-image ember-view"})
                        self.media_links.append(image_link['src'])
                        self.media_type.append("Image")
                    except:
                        try:
                            image_box = single_post.findAll("div",{"class": "feed-shared-image__single_post"})
                            image_link = image_box[0].find("img", {"class":"ivm-view-attr__img--centered feed-shared-image__image lazy-image ember-view"})
                            self.media_links.append(image_link['src'])
                            self.media_type.append("Image")
                        except:
                            try:
                                article_box = single_post.findAll("div",{"class": "feed-shared-article__description-single_post"})
                                article_link = article_box[0].find('a', href=True)
                                self.media_links.append(article_link['href'])
                                self.media_type.append("Article")
                            except:
                                try:
                                    video_box = single_post.findAll("div",{"class": "feed-shared-external-video__meta"})          
                                    video_link = video_box[0].find('a', href=True)
                                    self.media_links.append(video_link['href'])
                                    self.media_type.append("Youtube Video")   
                                except:
                                    try:
                                        poll_box = single_post.findAll("div",{"class": "feed-shared-update-v2__content overflow-hidden feed-shared-poll ember-view"})
                                        self.media_links.append("None")
                                        self.media_type.append("Other: Poll, Shared Post, etc")
                                    except:
                                        self.media_links.append("None")
                                        self.media_type.append("Unknown")
        
        
        
                view_single_post2 = set(single_post.findAll("li", {'class':["social-details-social-counts__item"]}))
                view_single_post1 = set(single_post.findAll("li", {'class':["social-details-social-counts__reactions","social-details-social-counts__comments social-details-social-counts__item"]}))
                result = view_single_post2 - view_single_post1
        
                view_single_post = []
                for i in result:
                    view_single_post += i
        
                try:
                    self.video_views.append(view_single_post[1].text.strip().replace(' Views',''))
        
                except:
                   self.video_views.append('N/A')
        
                
                try:
                    self.post_likes.append(new_likes[0].text.strip())
                except:
                    self.post_likes.append(0)
                    pass
        
                try:
                    self.post_comments.append(new_comments[0].text.strip())                           
                except:                                                           
                    self.post_comments.append(0)
                    pass
            
            except:
                pass
        return


    def date_conversion(self, row_date):
        d = row_date.split()
        val  = 0
        if (d[1] == 'minute') or (d[1] == 'minutes') or (d[1] == 'second') or (d[1] == 'seconds') or (d[1] == 'hour') or (d[1] == 'hours'):
            val = 0
        elif (d[1] == 'day') or (d[1] == 'days') : 
            val = 1
            
        elif (d[1] == 'week') or (d[1] == 'weeks'):
            val = 7
        elif (d[1] == 'month') or (d[1] == 'month'):
            val = 31
        else :
            val = 365
        
        gn_day     = int(d[0]) * val
        end_date   = datetime.datetime.utcnow()
        start_date = (end_date - datetime.timedelta(days=gn_day)).strftime("%m/%d/%Y")
        return start_date


    def plotting_df(self, freqs):
        df_words_used  = pd.DataFrame(sorted(freqs.items(), key = lambda word : word[1], reverse = True),  columns= ['words', 'counts'])
        first_25_rows  = df_words_used.loc[:self.top_n_words].reset_index(drop= True)
        return df_words_used, first_25_rows
    
    
    def analyze_words(self):
        
        """
        # call scrap func with df 
        """
        self.scrap_req_info(self.scrap_url())

        
        for i in self.post_comments:
            s = str(i).replace('Comment','').replace('s','').replace(' ','')
            self.comment_count += [s]
        
        data = {
                "Date Posted": self.post_dates,
                "Media Type": self.media_type,
                "Post Text": self.post_texts,
                "Post Likes": self.post_likes,
                "Post Comments": self.comment_count,
                "Video Views": self.video_views,
                "Media Links": self.media_links
                }
    
        df              = pd.DataFrame(data)   
        df['post_date'] = df['Date Posted'].apply(lambda x : self.date_conversion(x))
        
        #df.to_csv(str(PROJECT_DIR) + f'\\df_profile_{self.user_name}.csv')

        if self.period == 'all':
            df_subset = df.copy()
        else:
            df['post_date']                 = pd.to_datetime(df['post_date'])
            df_subset = df[df['post_date'] >= self.period].reset_index(drop= True)
        
        
    
        text_preprocess_cls          = PreprocessText()
        freqs                        = text_preprocess_cls.build_freqs(df_subset)
        df_words_used, first_25_rows = self.plotting_df(freqs)
        
        
        # fig = go.Figure()
        # fig.add_trace(go.Bar(x=first_25_rows.words, y=first_25_rows.counts, text=first_25_rows.counts, textposition="outside" ))
        # fig.update_xaxes(tickangle = 270,   title_text = "Words_commonly_used", title_font = {"size": 20}, title_standoff = 25)
        # fig.update_yaxes(title_text = "No of times",title_font = {"size": 20},title_standoff = 25)
        # fig.update_layout(title =  f'{self.user_name} - Top 30 Words usage in LinkedIn post from {self.period}')
        # plot(fig)

        
        return df_subset, df_words_used, first_25_rows



if __name__ == '__main__':  
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default = 'https://www.linkedin.com/in/satyanadella/', type=str, help = 'url_to_scrap the activity data')
    parser.add_argument('--period', default = 'all', type = str, help = 'scrap the data only until the mentioned period')
    parser.add_argument('--top_n_words', default = 50, type = int, help = 'Show Top N Words')
    args = parser.parse_args()
    
    # Call the class
    # call_class                                = LinkedInScrapper(url = args.url, period = args.period, top_n = args.top_n_words)
    # df_subset, df_words_used, first_25_rows   = call_class.analyze_words()
    
    
   