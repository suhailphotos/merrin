local LrApplication = import "LrApplication"
local LrDialogs = import "LrDialogs"

local Smart = {}

function Smart.run()
    local config = dofile(_PLUGIN.path .. "/Config.lua")
    local catalog = LrApplication.activeCatalog()

    local searchDesc = {
        combine = "intersect",
    }

    for _, rule in ipairs(config.smart.rules or {}) do
        table.insert(searchDesc, {
            criteria = rule.field,
            operation = rule.op,
            value = rule.value,
        })
    end

    local status = catalog:withWriteAccessDo(
        "Create Nested Smart Collection",
        function()
            local set1 = catalog:createCollectionSet(config.set1 or "Tests", nil, true)
            local set2 = catalog:createCollectionSet(config.set2 or "Ratings", set1, true)

            catalog:createSmartCollection(
                config.smart.name or "Unnamed",
                searchDesc,
                set2,
                true
            )
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
