#THIS IS A SCRAPY-LIKE PACKAGE

#THAT MEANS **THIS DIRECTORY** (aka the top-level bing_spiders dir) SHOULD ALWAYS BE YOUR WORKING DIRECTORY.

###HURRS SOME 'STRUCTUONS:

```python
>>> from bing_spiders import bing_news_2_csv
>>> bing_api_key = 'RAAAAAAAAANDOMNUMBERSANDLETTERFDAHJKFFADSHKFLDFAKHJ324HKJ2'
>>> myquery = 'unicorn sightings'
>>> bing_news_2_csv(bing_api_key, q=myquery, pages_of_links=20, csv_file_pth=None)
```

###NOW CHECK `bing_spiders.data.queries` THURS A CSV FILE THUR NOW ISN'T IT.

###OK NOW GET OUTTA IPYTHON N' GO BACK TO THE SHELL.

###NOW DO THIS:

```sh
$ pwd
 /path/to/bing_spiders
$ scrapy crawl bing_news
```


#THEN U DONE.