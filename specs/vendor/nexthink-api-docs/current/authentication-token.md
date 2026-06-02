# Getting an authentication token

The Nexthink APIs rely on a specific HTTP authentication scheme called [bearer authentication](https://swagger.io/docs/specification/authentication/bearer-authentication/) or token authentication. Get a token from the API using the Client Secret and Client ID generated earlier in the setup process.

Here are curl command examples:

<details>

<summary>zsh</summary>

{% code title="" overflow="wrap" %}

```zsh
curl --location "https://instance-login.region.nexthink.cloud/oauth2/default/v1/token" --header "Content-Type: application/x-www-form-urlencoded" --header "Authorization: Basic <Base64 encoded clientId:clientSecret>" --data-urlencode "grant_type=client_credentials" --data-urlencode "scope=service:integration"
```

{% endcode %}

</details>

<details>

<summary>powershell</summary>

{% code overflow="wrap" %}

```powershell
$headers = @{
  "Content-Type"  = "application/x-www-form-urlencoded"
  "Authorization" = "Basic <Base64 encoded clientId:clientSecret>"
}
$body = @{
  "grant_type" = "client_credentials"
  "scope"      = "service:integration"
}

$response = Invoke-RestMethod -Uri 'https://instance-login.region.nexthink.cloud/oauth2/default/v1/token' `
  -Method 'POST' `
  -Headers $headers `
  -Body $body `
  -ContentType 'application/x-www-form-urlencoded'

$response | ConvertTo-Json
```

{% endcode %}

</details>

<details>

<summary>cmd</summary>

{% code overflow="wrap" %}

```cmd
curl --location "https://instance-login.region.nexthink.cloud/oauth2/default/v1/token" --header "Content-Type: application/x-www-form-urlencoded" --header "Authorization: Basic <Base64 encoded clientId:clientSecret>" --data-urlencode "grant_type=client_credentials" --data-urlencode "scope=service:integration"
```

{% endcode %}

</details>

Replace `instance` by the name of the instance and `region` by the name of one of the following regions:

* `us` for the United States
* `eu` for the European Union
* `pac` for Asia-Pacific
* `meta` for the Middle East, Turkey and Africa

Replace `<Base64 encoded clientId:clientSecret>` with the Base64 token you generate from your `clientId` and `clientSecret` separated by a colon `:` .

#### Generating the Base64 token

In the example below, the value

* &#x20;`q2tj2fvyevr4z9djhkilhlmj3yw39tqpg` is the **clientId**, and&#x20;
* `cwbxklimy4k7qtnxohpbnueaydsuuhoftqza8tfzkykf` is the **clientSecret**.

The following examples show how to do this using the command-line interface (CLI)

<details>

<summary>zsh</summary>

{% code overflow="wrap" %}

```zsh
echo -n q2tj2fvyevr4z9djhkilhlmj3yw39tqpg:cwbxklimy4k7qtnxohpbnueaydsuuhoftqza8tfzkykf | base64
```

{% endcode %}

</details>

<details>

<summary>powershell</summary>

{% code overflow="wrap" %}

```powershell
[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes("q2tj2fvyevr4z9djhkilhlmj3yw39tqpg:cwbxklimy4k7qtnxohpbnueaydsuuhoftqza8tfzkykf"))
```

{% endcode %}

</details>

<details>

<summary>cmd</summary>

{% code overflow="wrap" %}

```cmd
powershell "[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes(\"q2tj2fvyevr4z9djhkilhlmj3yw39tqpg:cwbxklimy4k7qtnxohpbnueaydsuuhoftqza8tfzkykf\"))"
```

{% endcode %}

</details>

If the call is successful, the response is as follows, and the `access_token` field contains the token.

```json
{
    "token_type": "Bearer",
    "expires_in": 900,
    "access_token": "example",
    "scope": "service:integration"
}
```

The token has a 15-minute lifespan, after which you must request a new token.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/getting-authentication-token.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
