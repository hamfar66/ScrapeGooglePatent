# ScrapeGooglePatent
The code scrapes google patents urls with multi-thread and extracts title, abstract, inventors, and PDF download link.

To test the code:
1- Search for the term you want in Google Patent and then save all the links as a csv file in the Links folder using the Google Patent tool (a sample file test.csv exists in the directory for a faster test).
2- Specify the number of threads to run the code in parallel.
3- The output will be placed in the /files/split folder. A separate file is created for each thread (when each link is finished, it is deleted from the queue file and placed in the crawled file).
