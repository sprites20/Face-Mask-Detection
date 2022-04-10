
models["unmasked"] = {
	["model"] = <unmasked.model>
	["branches"] = {
		["employee1"] = <unmasked_employee1.model>,
		["employee2"] = <unmasked_employee2.model>,
	}
}
models["masked"] = {
	["model"] = <masked.model>
	["branches"] = {
		["employee1"] = <masked_employee1.model>,
		["employee2"] = <masked_employee2.model>,
	}
}

detected = {
	["masked"] = {},
	["unmasked"] = {},
}

function classify(image)
	--Do stuff
	return classification
end

function branchclassify(some_table)
	local result_classifications = {}
	for k,v in pairs(detected) do
		model = models[k][v]
		
		classname = classify(v, model)
		if result_classifications[classname] == nil then
			result_classifications[classname] = v
		end
	end
end

branchclassify(some_table)



	