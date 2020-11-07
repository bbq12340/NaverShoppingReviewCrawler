# NaverShoppingReviewCrawler
Keyword -> Links -> Scrape Review

How the program works
1. insert a keyword list (txt file)
2. scrapes smart-store links (by condition)
  - saves links to 'output/input.csv'
  - saves keywords with no result to 'output/none_keyword.txt'
3. scrapes list of reviews from each links
  - saves reviews to 'output/data/{file_name}.csv'
  *file_name is named by the item name. Special characters are replaced to '' by 're' module.
