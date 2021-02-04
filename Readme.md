## Selenium Bot

# Instructions

1. Install requirements with

```shell
 pip install -r requirements.txt
```

2. Copy settings_bkp.json to settings.json

```shell
 cp settings_bkp.json settings.json
```

3. Inside `settings.json`, change the proxy and chromedriver path

## To Avoid detection. Modify chrome driver

### For linux and mac

```shell
perl -pi -e 's/luc_/cat_/g' scraping/chromedriver
```

### For windows

```shell
perl -pi -e 's/luc_/cat_/g' scraping/chromedriver.exe
```

* Alternatively, You can opene the chromedriver in a text editor and replace `luc` with `anything`

## Run the main.py file