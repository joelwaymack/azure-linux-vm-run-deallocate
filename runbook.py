import sys
import azure.mgmt.resource
import azure.mgmt.compute
import automationassets
from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD

def get_automation_runas_credential(runas_connection, resource_url, authority_url ):
    """ Returns credentials to authenticate against Azure resoruce manager """
    from OpenSSL import crypto
    from msrestazure import azure_active_directory
    import adal

    # Get the Azure Automation RunAs service principal certificate
    cert = automationassets.get_automation_certificate('AzureRunAsCertificate')
    pks12_cert = crypto.load_pkcs12(cert)
    pem_pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pks12_cert.get_privatekey())

    # Get run as connection information for the Azure Automation service principal
    application_id = runas_connection["ApplicationId"]
    thumbprint = runas_connection['CertificateThumbprint']
    tenant_id = runas_connection['TenantId']

    # Authenticate with service principal certificate
    authority_full_url = (authority_url + '/' + tenant_id)
    context = adal.AuthenticationContext(authority_full_url)
    return azure_active_directory.AdalAuthentication(
        lambda: context.acquire_token_with_client_certificate(
            resource_url,
            application_id,
            pem_pkey,
            thumbprint)
    )

# Check for parameters
if len(sys.argv) < 4:
    exit('Missing required arguments!\nUsage: resource_group_name vm_name run_command', 1)

# Build parameters
resource_group_name = str(sys.argv[1])
vm_name = str(sys.argv[2])
run_command = str(sys.argv[3])

for count in range (4, len(sys.argv)):
    run_command += ' ' + str(sys.argv[count])

# Authenticate to Azure using the Azure Automation RunAs service principal
runas_connection = automationassets.get_automation_connection('AzureRunAsConnection')
resource_url = AZURE_PUBLIC_CLOUD.endpoints.active_directory_resource_id
authority_url = AZURE_PUBLIC_CLOUD.endpoints.active_directory
azure_credential = get_automation_runas_credential(runas_connection, resource_url, authority_url)

compute_client = azure.mgmt.compute.ComputeManagementClient(
    azure_credential,
    str(runas_connection['SubscriptionId']))

# Start the VM
print('Start VM')
async_vm_start = compute_client.virtual_machines.start(
    resource_group_name,
    vm_name)
async_vm_start.wait()
print('VM Started')

# Run the command
print('Running command')
run_command_parameters = {
    'command_id': 'RunShellScript',
    'script': [
        run_command
    ]
}

print('Command "' + run_command + '" will be executed on the VM.')

async_vm_run_command = compute_client.virtual_machines.run_command(
    resource_group_name,
    vm_name,
    run_command_parameters
)

print(async_vm_run_command.result().value[0].message)

print('Command executed')