import requests, json


# #  OPTION 1. # # # # #  A SINGLE SMILE AS A TEXT. THE OUTPUT IS A JSON   # # # # #

query = {
	"account_token": "1JX3LP",
	"account_secret_key": "A8X9641JM",
	"account_user": "OOntox",
	"module": "ProtoPHYSCHEM",
	"input_type": "SMILES_TEXT",
	"input_data": "CCCCC",
  	"models_list": "model_phys:water_solubility,model_phys:melting_point"
}

response = requests.post("https://protopred.protoqsar.com/API/v2/", data=query)

with open(r"output_option1.json", "w") as f:
	json.dump(response.json(), f, indent=4, ensure_ascii=False)

print(response.json())

json_string = response.headers["X-Extra-JSON"]
json_response = json.loads(json_string)
print(json_response)




# # OPTION 2. # # # # #  FILE UPLOAD (EXCEL OR JSON). THE REQUEST NEEDS THE PARAMETER "file". THE OUTPUT IS A JSON   # # # # # 


query = {
	"account_token": "1JX3LP",
	"account_secret_key": "A8X9641JM",
	"account_user": "OOntox",
	"module": "ProtoPHYSCHEM",
	"input_type": "SMILES_FILE",
	"models_list": "model_phys:water_solubility, model_phys:melting_point",
}

# # # # # XLSX file # # # # #
file_path = "input.xlsx"

# # # # # JSON file # # # # #
# file_path = "JSON_input.json"

files = {"input_data": open(file_path, "rb")} 

response = requests.post("https://protopred.protoqsar.com/API/v2/", data=query, files=files)


with open(r"output_option2.json", "w") as f:
	json.dump(response.json(), f, indent=4, ensure_ascii=False)

print(response.json())

json_string = response.headers["X-Extra-JSON"]
json_response = json.loads(json_string)
print(json_response)





# # OPTION 3. # # #  FILE UPLOAD (EXCEL OR JSON). THE REQUEST NEEDS THE PARAMETER "file". THE OUTPUT IS AN EXCEL (XLSX)  # # # #


query = {
	"account_token": "1JX3LP",
	"account_secret_key": "A8X9641JM",
	"account_user": "OOntox",
	"module": "ProtoPHYSCHEM",
	"input_type": "SMILES_FILE",
	"models_list": "model_phys:water_solubility, model_phys:melting_point",
	"output_type": "XLSX"
}

# # # # # XLSX file # # # # #
# file_path = "input.xlsx"

# # # # # JSON file # # # # #
file_path = "JSON_input.json"

files = {"input_data": open(file_path, "rb")} 

response = requests.post("https://protopred.protoqsar.com/API/v2/", data=query, files=files)

with open(r"output_option3.xlsx", "wb") as f:
	f.write(response.content)

json_string = response.headers["X-Extra-JSON"]
json_response = json.loads(json_string)
print(json_response)




# # OPTION 4 # # # # #  EMBEDDED JSON IN THE REQUEST BODY. THE OUTPUT IS A JSON  # # # # # #


query = {
	"account_token": "1JX3LP",
	"account_secret_key": "A8X9641JM",
	"account_user": "OOntox",
	"module": "ProtoPHYSCHEM",
	"input_type": "SMILES_FILE",
	"models_list": "model_phys:water_solubility, model_phys: melting_point",
	"input_data": 
		 	{
				"ID_1": {
					"SMILES": "C1=CC(=O)C=CC1=O"
				},
				"ID_2": {
					"SMILES": "CCCCC",
					"CAS": "10-66-0",
					"Chemical name": "Pentane",
					"EC number": "203-692-4",
					"Structural formula": "C5H12"
				},
				"ID_3": {
					"SMILES": "O=[N+]([O-])c1ccc2nc[nH]c2c1",
					"CAS": "94-52-0",
					"Chemical name": "6-nitro-1H-benzimidazole",
					"EC number": "202-341-2",
					"Structural formula": "C7H5N3O2"
				}
			}
}

response = requests.post("https://protopred.protoqsar.com/API/v2/", json=query)


with open(r"output_option4.json", "w") as f:
	json.dump(response.json(), f, indent=4, ensure_ascii=False)

print(response.json())

json_string = response.headers["X-Extra-JSON"]
json_response = json.loads(json_string)
print(json_response)






# # OPTION 5 # # # # #   THE DATA IS PROVIDED BY LOADING A JSON FILE. THE OUTPUT IS A JSON  # # # # #


query = open("request_body_API.json", "rb")

response = requests.post("https://protopred.protoqsar.com/API/v2/", data=query)


with open(r"output_option5.json", "w") as f:
	json.dump(response.json(), f, indent=4, ensure_ascii=False)

print(response.json())

json_string = response.headers["X-Extra-JSON"]
json_response = json.loads(json_string)
print(json_response)