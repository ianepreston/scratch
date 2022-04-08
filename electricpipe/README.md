# Let's build a data pipeline

I want to test out some different ways of building a data pipeline. The goal of this repository is to learn some new tools, not so much to do a cool data analysis. To that end I'm going to just grab some [electricity data](https://api.aeso.ca/web/api/ets) and see how many different tools I can push it through. Besides the pipeline itself the other thing I'm interested in learning here is how to reproducibly deploy the pipeline. For that I'll be using [terraform](https://www.terraform.io/)

## Setting up my local environment

Besides terraform I want to deploy this pipeline to Azure, so I will need some Azure tools installed:

### Install Azure CLI

Instructions from [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli). This is what they recommended at the time I was working on this:

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
# Log in to Azure
az login
```

### Install Azure functions CLI

Instructions from [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Clinux%2Ccsharp%2Cportal%2Cbash#v2=). This is what they recommended at the time I was working on this:

```bash
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'
sudo apt update && sudo apt install azure-functions-core-tools-4
```

### Install Terraform

Instructions from [here](https://www.terraform.io/downloads). This is what they recommended at the time I was working on this:

```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform
```


## Set up a function app and functions

I've built function apps before but I had a very manual deployment process, and if I didn't like something there was no easy way to automatically tear it all down and start again. I'm going to try and resolve that by doing it all with terraform. Setting up the app code structure is outside the scope of terraform though so I'll build a "hello world" example 

```bash
# Set up python environment for the functions
pyenv local 3.10.2
python -m venv .venv
source .venv/bin/activate
# Set up the function app
func init electricfunc --python
# Create a function within the function app
cd electricfunc/
func new --name helloworld --template "HTTP trigger" --authlevel "anonymous"
```

## Annoying caveat I found about terraform

If a terraform job fails halfway through an "apply" then it won't clean up the previous steps. As an example when I first tried to apply this function app it built 3 things and then failed on the 4th because something in my config wasn't available in the region I'd selected (Canada Central). I figured the easiest fix would be to update the config to "US East" since that was what the example I was following used and rerun ```terraform apply```. This resulted in an error though because I already had a resource group of the same name in Canada Central and it couldn't create a new one in US East. I had assumed it would update the existing resources with my new configuration, but for some reason that wasn't saved. I ended up reverting my location back to Canada Central, running ```terraform destroy``` to clean up, manually checking in Azure that everything was gone, and then re-running with the new location. See [this post](https://community.gruntwork.io/t/cleanup-of-terraform-apply-partial-fails/420) for a discussion.

## Actually deploying functions using terraform

Terraform is not actually configured to deploy functions themselves, just the surrounding infrastructure like storage accounts and function apps. However, we can extend it with a local executor to deploy the function as part of the build. The full code is in ```terraform/main.tf``` but here's the relevant snippet:

```terraform

resource "null_resource" "functions" {

  triggers = {
    functions = "${local.func_app_version}_${join("+", [for value in local.func_app_functions : value["name"]])}"
  }
  # Seems we have to wait a bit after the function app is created before the publish command will work
  provisioner "local-exec" {
    command = "sleep 10; cd ../electricfunc; func azure functionapp publish ${azurerm_function_app.function_app.name}; cd ../terraform"
  }
}
```

Note that I had to hack in a sleep command before the function deploy, as otherwise I ran into issues where the function app wasn't quite ready by the time the command to publish a function was executed. The ```config.yaml``` file placed in the function app directory of this repository is where I indicate to terraform that the function itself has been changed and needs to be redeployed.


# Resources I consulted while working on this

In approximately chronological order here are the sites I looked at while building this (except official docs)

* https://medium.com/datasparq-technology/how-to-deploy-a-python-function-app-in-azure-with-terraform-68af428a6c9a
* https://dev.to/kemurayama/deploying-azure-functions-for-python-with-terraform-n
* https://adrianhall.github.io/typescript/2019/10/23/terraform-functions/
* https://www.maxivanov.io/deploy-azure-functions-with-terraform/
* https://www.maxivanov.io/publish-azure-functions-code-with-terraform/
* https://medium.com/pernod-ricard-tech/how-to-properly-manage-secrets-in-azure-app-service-with-terraform-44bc1ab99a02