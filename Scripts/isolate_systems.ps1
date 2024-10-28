# PowerShell script to isolate affected systems
# This script requires administrator privileges to execute

param (
    [string[]]$CompromisedSystems
)

# Function to isolate a compromised system
function Isolate-System {
    param (
        [string]$ComputerName
    )
    try {
        # Disable network adapter to isolate the system
        $networkAdapters = Get-WmiObject -Class Win32_NetworkAdapter -ComputerName $ComputerName -Filter "NetEnabled=True"
        foreach ($adapter in $networkAdapters) {
            $adapter.Disable()
            Write-Host "Successfully disabled network adapter on system: $ComputerName"
        }
    }
    catch {
        Write-Error "Failed to isolate system: $ComputerName. Error: $_"
    }
}

if ($CompromisedSystems.Count -eq 0) {
    Write-Error "No compromised systems provided. Please specify the systems to isolate."
    exit 1
}

foreach ($ComputerName in $CompromisedSystems) {
    Isolate-System -ComputerName $ComputerName
}
