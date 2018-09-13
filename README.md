# Indexa Analysis
This is a [dash](https://plot.ly/products/dash/) app that analysis some funds from [Indexa capital](https://indexacapital.com/es).

It is possible to see a live demo here: [expensor_heroku](https://indexa-analysis.herokuapp.com/)

Some screenshots of the app:

![Screenshoot_1](assets/screenshot_1.png)
![Screenshoot_2](assets/screenshot_2.png)
![Screenshoot_3](assets/screenshot_3.png)

## Instructions
At this moment the data is not automatically updated. I might update it at some point or I m
If you want **to update the data** you should:
1. Download funds data from financial times. For example: https://markets.ft.com/data/funds/tearsheet/historical?s=IE00B04FFJ44:EUR
2. Get an indexa_capital token and store it as an evironment variable called `INDEXA_TOKEN`
3. Run "python get_data.py". This will update the file `data/indexa.xlsx`

And for **running the app locally** you will need to run the following commands from the source path:
1. `pip install -r requirements.txt`
2. `python src/index.py`

## Authors
* [Arnau Villoro](villoro.com)

## License
The content of this repository is licensed under a [MIT](https://opensource.org/licenses/MIT).

## Nomenclature
Branches and commits use some prefixes to keep everything better organized.

### Branches
* **f/:** features
* **r/:** releases
* **h/:** hotfixs

### Commits
* **[NEW]** new features
* **[FIX]** fixes
* **[REF]** refactors
* **[PYL]** [pylint](https://www.pylint.org/) improvements
* **[TST]** tests