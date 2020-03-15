# nertflix-app

This is a web app which will crawl the [website](https://www.whats-on-netflix.com/) for new shows on netflix,
and shows that are coming soon to netflix. It represents the results in a nice table, 
and can even send it to a list of email addresses.

## Instructions
1. clone the repo locally
2. edit the `settings.yml` file to select which shows you want to see (by rating, genre, language, etc...)
3. create a gmail account to send the emails
4. build the container with the following `--build-arg`s:
  * `GMAIL_USER` - the username for the account you just created
  * `GMAIL_PASSWORD` - the password for the account you just created
  * `EMAILS` - a string of email addresses separated by `' '`
5. run the docker container and expose port `5000`

## Crawling
* new netflix content - http://0.0.0.0:5000/crawl/new_content
* coming soon to netflix - http://0.0.0.0:5000/crawl/coming_soon

## Show Results
* new netflix content - http://0.0.0.0:5000/results/new_content
* coming soon to netflix - http://0.0.0.0:5000/results/coming_soon

## Send Emails
* new netflix content - http://0.0.0.0:5000/send_mail/new_content
* coming soon to netflix - http://0.0.0.0:5000/send_mail/coming_soon

**Note**: in order to show the results or send emails, you must first crawl the requested content type.

You may upload the container to a remote cluster and schedule the app to crawl and send emails (I used gcloud run).
