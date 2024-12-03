# requirements
- openai api key (card payment)
- asana api key (no payments required)
- google api key (no payments required)

# installation instructions
in terminal 

- navigate to repo folder
- run follwing commands
```chmod +x install.sh run.sh```

```./install.sh```
```./run.sh``

## get your api keys
- openai api key  https://platform.openai.com/api-keys 
- asana api personal access token https://app.asana.com/0/my-apps
- google api key https://support.google.com/googleapi/answer/6158862?hl=en

# naming conventions

functions named 'fetch_something' refer to api get requests, and return internal objects
functions named 'get_something' refer directly to existing internal program objects