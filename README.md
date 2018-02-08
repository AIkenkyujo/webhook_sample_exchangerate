# DialogFlow - sample webhook in Python

AI研究所チャットボット入門セミナー用プログラムです。  
It is a program created for use at the AI-Kenkyujo seminar.

More info about DialogFlow webhooks could be found here:
[DialogFlow Webhook](https://docs.DialogFlow/docs/webhook)

# Deploy to:
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# What does the service do?
It's a exchange rate information fulfillment service that uses [currencylayer](https://currencylayer.com/).
The services takes the `currency` parameter from the action, performs exchange rate information.

The service packs the result in the DialogFlow webhook-compatible response JSON and returns it to DialogFlow.

## License
See [LICENSE](LICENSE).
