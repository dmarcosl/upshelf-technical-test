## Upshelf Technical Test

This is my solution to the technical test of Upshelf

I used the current version of Scrapy (2.5.1)

In [main.py](./main.py) is the execution with the Scrapy Crawler Process, and in [project/spiders/target_com.py](./project/spiders/target_com.py) is the extraction logic for the given url. I also edit the [project/spiders/pipelines.py](./project/pipelines.py) file to input the title of the scraped items at the end.

### Statement

Please scrape https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109#lnk=sametab using ONLY Scrapy. 

Fields:
   - price
   - description
   - specifications
   - highlights
   - questions
   - images urls
   - title
 
Output of the item is simple console print. Push the final solution in the github. Let me know whenever you have completed the assessment as well, please.