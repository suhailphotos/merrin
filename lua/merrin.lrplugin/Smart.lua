local LrApplication = import "LrApplication"
local LrDialogs = import "LrDialogs"

local Smart = {}

local function copyRules(rules)
    local out = {}
    for _, rule in ipairs(rules or {}) do
        table.insert(out, {
            field = rule.field,
            op = rule.op,
            value = rule.value,
        })
    end
    return out
end

local function mergeRules(parentRules, localRules)
    local merged = copyRules(parentRules)
    for _, rule in ipairs(localRules or {}) do
        table.insert(merged, {
            field = rule.field,
            op = rule.op,
            value = rule.value,
        })
    end
    return merged
end

local function buildSearchDesc(matchMode, rules)
    local combine = "intersect"
    if matchMode == "any" then
        combine = "union"
    end

    local searchDesc = {
        combine = combine,
    }

    for _, rule in ipairs(rules or {}) do
        table.insert(searchDesc, {
            criteria = rule.field,
            operation = rule.op,
            value = rule.value,
        })
    end

    return searchDesc
end

local function createSmartCollections(catalog, parentSet, smartDefs, inheritedRules)
    for _, smartDef in ipairs(smartDefs or {}) do
        local combinedRules = mergeRules(inheritedRules, smartDef.rules or {})
        local searchDesc = buildSearchDesc(smartDef.match or "all", combinedRules)

        catalog:createSmartCollection(
            smartDef.name or "Unnamed",
            searchDesc,
            parentSet,
            true
        )
    end
end

local function walkGroup(catalog, parentSet, node, inheritedRules)
    local currentSet = catalog:createCollectionSet(node.name or "Unnamed", parentSet, true)
    local currentRules = mergeRules(inheritedRules, node.rules or {})

    if node.smart then
        createSmartCollections(catalog, currentSet, node.smart, currentRules)
    end

    for _, child in ipairs(node.children or {}) do
        walkGroup(catalog, currentSet, child, currentRules)
    end
end

function Smart.run()
    local config = dofile(_PLUGIN.path .. "/Config.lua")
    local catalog = LrApplication.activeCatalog()

    local status = catalog:withWriteAccessDo(
        "Build Merrin Collections",
        function()
            for _, group in ipairs(config.groups or {}) do
                walkGroup(catalog, nil, group, {})
            end
        end,
        { timeout = 15 }
    )

    LrDialogs.message(
        "Merrin",
        "Write status: " .. tostring(status),
        "info"
    )
end

return Smart
