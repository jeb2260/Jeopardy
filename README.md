Usage
-----

#### `npm install`

#### `npm start`


Back End (Data Collection)
-----

download.py - creates a folder of .html files of every
episode of particular Jeopardy season(s) called 
"j-archive archive", using data from www.j-archive.com

j-archive-parser.py - Parses the episodes in "j-archive
archive" and creates a csv file for an entire season in 
the folder "j-archive-csv". This csv contains every 
game, clue, and result of the season.

-Note: Only have done a portion of season 36 (current season)
so far. Once I'm sure everything works for season 36, I'll add in 
previous seasons and the challenges that come with that

j-archive-podiums.py - Organizes data from the season csv
into a "game log" csv titled "podium-data.csv". Contains
contestant names and their overall/round performances

categories.py - First aggregates how contestants performed
on a category in a particular game in "category-data.csv".
Then, aggregates all-time category performance in "categories.csv"

contestants.py - Aggregates overall contestant performance (throughout
their run) in contestant-profiles.csv

categoryjson.py - Does same thing as categories.py but outputs data
as a JSON file instead of a csv (needed for front-end)

contestantjson.py - Does same thing as contestants.py but outputs data
as a JSON file instead of a csv (needed for front-end)

Front End (jwebsite folder)
-----

Written in ReactJS 

App.js renders home page, which is currently a search bar and a footer 
(similar to WolframAlpha) 

To search for a contestant, you search their full name (case-insensitive).
(You can also do "contestant: (name)" as your search query. Potentially
useful in the future in case you want to search up "John Smith" and want
the search engine to know you want the contestant and not clues
about/containing "John Smith"). Rendered by Contestant.js

To search for a category, same thing as before, with optional "category: "
keyword. Rendered by Category.js

Search.js gets appropriate results from "data" file containing categories.json
and contestants.json

For example, search "jason zuffranieri" and see what happens

To-Do List (exhaustive, not in any particular order)
--------

- [ ] Make search bar work for questions (“Who has the second-highest total without winning?”) etc —> business logic here (“Who”—> contestant, “most”—> max function, etc). End goal, save for later
- [ ] Give users filters that are easy to manipulate (only season 36, only 100+ clues answered, only Final Jeopardies)
- [ ] Give user an option to display data in table form (like baseball-reference)
- [ ] Fill out text for legal/about/contact (make an email/form so former contestants can email if they don’t like their picture or would like to offer a correction)
- [ ] Create “tab” for Alex, the GOATS, Tournament info. Make tabs like binder tabs on top of search bar (so first tab that is auto-selected is “Search”)
- [ ] Look at baseball-reference to see what else to add on a contestant’s category page
- [ ] Adblock (getting errors here, not sure why)
- [ ] Manually label categories into genres/sub-genres 
(so if someone wants to know how contestants perform on Geography categories,
it'll aggregate data from "Middle East Geography" and "South American Geography" categoryes). Will be pretty labor-intensive honestly but fun for me
- [ ] Look up how to connect Python back-end (if data doesn’t exist, run script with user parameters and then get json file and corresponding data)
- [ ] Make website auto-update every day at a certain time (so games are up-to-date)
- [ ] Give contestants an area for their achievements, like the rectangles on 
the top right here: https://www.baseball-reference.com/players/t/troutmi01.shtml
- [ ] Duplicate names!!!! How to deal with it (unique Id for people somehow…)
- [ ] Add pictures for everyone
- [ ] Add margin of victory/lock games
- [ ] General styling of the website (I suck)