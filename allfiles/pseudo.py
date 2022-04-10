models = {
  "masked" : {
      "model" : "masked.model",
      "branches" : {
          "employee1" : {
              "model" : "masked_employee1.model",
              "branches" : {},
          },
          "employee2" : {
              "model" : "masked_employee2.model",
              "branches" : {},
          },
      },
  },
  "unmasked" : {
      "model" : "unmasked.model",
      "branches" : {
          "employee1" : {
              "model" : "unmasked_employee1.model",
              "branches" : {},
          },
          "employee2" : {
              "model" : "unmasked_employee2.model",
              "branches" : {},
          },
      },
  },
}

detected = {
	"masked" : {},
    "unmasked" : {},
}

def classify(image, model):
	classification = ""
	return classification

def branchdetect(sometable, table2):
	result = {}
	for k,v in sometable.items():
		currentbranch = table2[k]["branches"]
		print(k)
        
branchdetect(detected, models)



	



	