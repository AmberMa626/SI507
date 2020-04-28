# SI507
<b>Instructions for running code:</b><br/>
It includes three python file and a Data directory.<br/> 
(1)	You can use the scrape.py to scrape all of the data, if you want to update the data, you can delete the cache.json and re-run this python file, it will generate 4 json into data directory. Please also download the show_theater.csv which includes junction table key of musical and theater, because they are many to many relationship, we need junction table key to connect those two tables. You also need to get Yelp Fusion API key and client ID by creating an app on Yelp’s Developers site and put them in a python file named secrets.py. Please refer to this link: https://www.yelp.com/developers/documentation/v3/authentication.<br/> 
(2)	You can run the database.py to update the Browdway_touring_theater.sqlite and import data from Data directory. Or you can use the created database.<br/> 
(3)	You can run the app.py to use the Flask App. Please put the templates directory, Browdway_touring_theater.sqlite(database) and app.py together.<br/> 


<b>Description of how to interact with the program:</b><br/> 
Please download app.py, templates directory, and Browdway_touring_theater.sqlite(database) to run the app. <br/> 
There’re three buttons in the main page: get theaters, get other musicals, and get restaurants.<br/> 
For the first button, users can input musical name to the touring theaters available for this musical and theaters’ detailed information, such as city, state, address, zip code, official website link. Users can return to the main page by Home button. If no information shows up, users can re-enter a valid musical name.<br/> 
For the second button, users can input theater name to see all of the upcoming musicals that will be performed in the input theater. If no information shows up, users can  re-enter a valid touring theater name.<br/> 
For the third button, users can choose the theater in select list and see recommended restaurants nearby. Users also can choose how to sort the results, the options include ratings, price, and review counts. The sort direction also includes high to low and low to high. <br/> 
If users click get restaurants directly, it will show a table including restaurant name, phone number, location, etc. If users choose Bar chart or Histogram, it will show different data visualization.
