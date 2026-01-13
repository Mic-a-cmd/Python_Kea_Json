# Szenario: Du hast eine bestehende kea-dhcp4.json. Bearbeite die Datei gemäß den folgenden Anweisungen.

# Hier kommt der Code

import json

with open('kea-dhcp4.json') as line:
    dhcp_dict = json.load(line)

print("\nDie vorliegende .json-Datei sieht (in einer Zeile geschrieben) folgendermaßen aus:")
print(dhcp_dict.values())

# Teil 1: Analyse (Read-only)
#
# Lifetime: Ermittle den Wert für die valid-lifetime.

print("\nTeil 1:\n")
print(list(dhcp_dict["Dhcp4"].keys())[3], "=", dhcp_dict["Dhcp4"]["valid-lifetime"])

# Inventur: Wie viele subnet4-Blöcke sind aktuell konfiguriert?
print("Aktuell konfigurierte subnet4-Blöcke =", len(dhcp_dict["Dhcp4"]["subnet4"]))

# Identifikation: Welche id hat das erste Subnetz im Array?
print("ID des 1. Subnetzes im Array =", dhcp_dict["Dhcp4"]["subnet4"][0]["id"])

# Teil 2: Modifikation des ersten Subnetzes
#
# Netzwerk: Ändere das Subnetz des ersten Eintrags auf 10.101.101.0/24.

print("\nTeil 2:\n")
print("subnet", dhcp_dict["Dhcp4"]["subnet4"][0]["subnet"], "wird geändert in: ", end="")
dhcp_dict["Dhcp4"]["subnet4"][0]["subnet"] = "10.101.101.0/24"
print(dhcp_dict["Dhcp4"]["subnet4"][0]["subnet"])

# Address-Pools: Passe die pools so an, dass sie innerhalb des neuen Subnetzes liegen (z. B. .10 bis .100).
print("pool", dhcp_dict["Dhcp4"]["subnet4"][0]["pools"][0]["pool"], "wird geändert in: ", end="")
dhcp_dict["Dhcp4"]["subnet4"][0]["pools"][0]["pool"] = "10.101.101.10-10.101.101.100"
print(dhcp_dict["Dhcp4"]["subnet4"][0]["pools"][0]["pool"])

# Standard-Optionen: * Ändere die IP-Adresse des routers und der domain-name-servers passend zum neuen Subnetz.
print("data/routers", dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][0]["data"], "wird geändert in: ", end="")
dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][0]["data"] = "10.101.101.254"
print(dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][0]["data"])
print("und")
print("data/domain-name-servers", dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][1]["data"], "wird geändert in: ",
      end="")
dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][1]["data"] = "10.101.101.254"
print(dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][1]["data"])
print()

# Setze den domain-name und domain-search auf deine eigene Domain (z.B. meinefirma.local).
print("data/domain-name", dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][2]["data"], "wird geändert in: ", end="")
dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][2]["data"] = "mic-a-linux.zz"
print(dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][2]["data"])
print("und")
print("data/domain-search", dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][3]["data"], "wird geändert in: ", end="")
dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][3]["data"] = "mic-a-linux.zz"
print(dhcp_dict["Dhcp4"]["subnet4"][0]["option-data"][3]["data"])
print()

# Bereinigung: Entferne den gesamten Konfigurationsblock "dhcp-ddns".
del dhcp_dict["Dhcp4"]["dhcp-ddns"]
print("Nach Entfernung des Konf.-blocks \"dhcp-ddns\":")
print(dhcp_dict.values())

# Teil 3: Erweiterung und Global-Settings
#
# Neues Subnetz anlegen: Füge ein zweites Subnetz-Objekt mit folgenden Daten hinzu:
# id: 2
# subnet: 192.168.0.0/24
# pools: 192.168.0.10 - 192.168.0.100
# Sicherstellung der expliziten Bindung Subnetz 1  (10.101) an eth0
#                               key value pair "interface" : "eth0"
# Sicherstellung der expliziten Bindung Subnetz 2 (192.168) an eth1
#                               key value pair "interface" : "eth1"

print("\nTeil 3:\n")

# Hier vorab die explizite Bindung Subnetz 1 an "eth0":
dhcp_dict["Dhcp4"]["subnet4"][0]["interface"] = "eth0"

# Da durch "Neues Subnetz anlegen" eine Menge Zeilen einzugeben wären,
# wird verkürzt durch Kopieren des ersten Subnetz-Objekts und
# Anpassung maßgeblicher Zeilen im neu erstellten Subnetz-Objekt:
import copy
copy_block = dict(dhcp_dict["Dhcp4"]["subnet4"][0])
print("Der Ursprungs-Block sieht folgendermaßen aus:")
print(copy_block)
new_block = copy.deepcopy(copy_block)
# Anhängen des neuen Blocks
dhcp_dict["Dhcp4"]["subnet4"].append(new_block)
new_block["id"] = 2
new_block["subnet"] = "192.168.0.0/24"
new_block["pools"][0]["pool"] = "192.168.0.10-192.168.0.100"
new_block["option-data"][0]["data"] = "192.168.0.254"
new_block["option-data"][1]["data"] = "192.168.0.254"
new_block["interface"] = "eth1"

print("Der neue Block sieht folgendermaßen aus:")
print(new_block)

print("\nDie mic-a_kea.json-Datei sieht (in einer Zeile geschrieben) folgendermaßen aus:")
print(dhcp_dict.values())

print("\n\"eth1\" wird unter \'interfaces\' hinzugefügt:", dhcp_dict["Dhcp4"]["interfaces-config"]["interfaces"])

# Interface-Binding: * Passe das globale interfaces-config Array so an, dass es auf ["eth1", "eth2"] lauscht.
dhcp_dict["Dhcp4"]["interfaces-config"]["interfaces"].append("eth1")



with open('mic-a_kea.json', 'w') as f:
    f.write(json.dumps(dhcp_dict))
