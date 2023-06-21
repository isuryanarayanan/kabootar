**Kabootar - Simplify Transactional Messaging Integration**

Using genie for running your project
```bash
$ git clone git@github.com:isuryanarayanan/kabootar.git
$ chmod +x ./genie.sh
$ ./genie.sh
```

or run it directly

```bash
$ docker compose -f conf/local/docker-compose.yml up
```


Kabootar is an open-source Python package that simplifies the integration of transactional messaging services like email and SMS into your applications. It provides a unified API for seamless integration and offers features like template management and event-driven messaging. Easily send transactional messages using different messaging platforms with Kabootar.

**Key Features:**
- Seamless integration with email and SMS services.
- Manage message templates and customize them with dynamic data.
- Automate message sending with event-driven messaging.
- Secure secrets management for API keys and credentials.
- Flexible configuration to adapt to project requirements.

**Requirements:**
- Kabootar requires the Serverless Framework CLI to be installed. You can install it by following the instructions provided at [Serverless Framework](https://www.serverless.com/framework/docs/getting-started/).

**Getting Started:**
- Install Kabootar using `pip install kabootar`.
- Follow the documentation and examples for integrations and template management.
- Start sending transactional messages in your applications effortlessly.

**Contributing:**
- Contributions, bug reports, and feature requests are welcome! Please review our contribution guidelines before making any contributions.

**License:**
- Kabootar is released under the MIT License. See the `LICENSE` file for more details.
