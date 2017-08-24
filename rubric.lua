Row = {}

function Row:new(title, weight)
	o = { title=title, weight=weight, criteria={} }
	setmetatable(o, self)
	self.__index = self
	return o
end

function Row:addSingle(index, str)
	crit = self.criteria[index] or ""
	if crit ~= "" then
		crit = crit .. "\\par "
	end
	crit = crit .. str
	self.criteria[index] = crit
	return self
end
	
function Row:addRepeated(startIndex, count, str)
	for i = startIndex, startIndex+count-1 do
		self:addSingle(i, str)
	end
	return self
end
	
function Row:addMultiple(startIndex, args)
	for i,par in ipairs(args) do
		self:addSingle(startIndex + i - 1, par)
	end
	return self
end
	
function Row:addFormatted(startIndex, fmt, args)
	for i,par in ipairs(args) do
		self:addSingle(startIndex + i - 1, string.format(fmt, par))
	end
	return self
end
	
function printRubric(rubric)
	totalWeight = 0
	for rowIndex, row in ipairs(rubric) do
		totalWeight = totalWeight + row.weight
	end
	
	if totalWeight ~= 100 then
		tex.print("\\rubrictitle{Marking Rubric --- FIXME: weights add up to ", totalWeight, " and not 100!}")
	end
	
	tex.print("\\begin{markingrubric}")
	
	for rowIndex, row in ipairs(rubric) do
		if rowIndex == 1 then
			tex.print("\\firstcriterion")
		else
			tex.print("\\criterion")
		end
		
		tex.print(string.format("{%s}{%d\\%%}", row.title, row.weight))
		
		for i = 0,5 do
			if row.criteria[i] ~= nil then
				span = 1
				while i + span <= 5 and row.criteria[i + span] == nil do
					span = span + 1
				end
				
				if span > 1 then
					tex.print(string.format("\\gradespan{%d}{%%", span))
				else
					tex.print("\\grade")
				end
				
				if i == 0 then
					tex.print("\\fail")
				end
				
				tex.print(row.criteria[i] or "")
				
				if span > 1 then
					tex.print("}")
				end
			end
		end
	end
	
	tex.print("\\end{markingrubric}")
end
